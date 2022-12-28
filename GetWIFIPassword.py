import subprocess, platform,os

if platform.system() == "Windows":
    data = subprocess.check_output(['netsh','wlan','show', 'profiles']).decode('utf8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

    for i in profiles:
        results = subprocess.check_output(['netsh','wlan','show', 'profile',i,'key=clear']).decode('utf8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

    try:
        print("{:<30}| {:<}".format(i,results[0]))
    except:
        print("{:<30}| {:<}".format(i,""))

elif platform.system() == "Linux":
    terminalCommand = "sudo grep psk= /etc/NetworkManager/system-connections/*"
    password = os.popen(terminalCommand).read().split("\n")[0].split("=")[1]
    print(password)
else:
    print("Only Windows and Linux are supported.")