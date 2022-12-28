import smtplib

sender = "aladinaladin644@gmail.com"
password = "Assassin1@"
receiver = "t.ivanov2003@abv.bg"

connection = smtplib.SMTP("smtp.gmail.com", 587)
connection.starttls()
connection.login(user = sender, password = password)

connection.sendmail(from_addr = sender, to_addr = receiver, msg = "Python sent message")
connection.close()