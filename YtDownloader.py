from pytube import YouTube
from pytube import Stream
from tkinter import *
from tkinter import ttk

def OnProgress(stream:Stream, chunk: bytes, bytes_remaining: int):
    bytes_downloaded = stream.filesize - bytes_remaining
    percentage_completion = bytes_downloaded/stream.filesize * 100
    
    if(bytes_remaining > 0):
        print("Progress: {0:0.1f}%".format(percentage_completion))
    
def OnDownloadComplete(arg1,arg2):
    print("Video downloaded!")

def DownloadVideo(video_link:str,resolution:str):
    try:
        yt_instance = YouTube(video_link)
        yt_instance.register_on_progress_callback(OnProgress)
        yt_instance.register_on_complete_callback(OnDownloadComplete)

        ytStream = yt_instance.streams.filter(file_extension="mp4",resolution=resolution).first()
        ytStream.download(output_path="./yt_downloads")

    except: print("Error downloading video")

def Init():
    global root 
    root = Tk()
    root.resizable(width=False,height=False)
    root.title("YouTube Downloader")
    root.geometry("640x480")

    ttk.Label(root, text="Enter a video link").grid(column=1, row=2,padx=20)
    global video_link_text
    video_link_text = Text(root, height=1, width=35)
    video_link_text.grid(column=1,row=3)
    video_link_text.bind("<KeyRelease>",SelectVideo)

    root.grid_rowconfigure(10, weight=1)
    ttk.Button(root, text="Quit", command=root.destroy).grid(row=10,column=3,sticky="es")
    #add button when stopped writing and input is a link
    root.mainloop()

selectedResolution = ""
videoLink = ""

def SelectVideo(selectedVideoLink:str):
    videoLink = selectedVideoLink
    combobox = ttk.Combobox(root,textvariable="360p")
    combobox['values'] = ('144p', '240p', '360p', '480p', '720p', '1080p')
    combobox['state'] = 'readonly'
    combobox.bind('<<Selected>>', SelectResolution)
    combobox.grid(column=2,row=3)

def SelectResolution(resolution:str):
    selectedResolution = resolution
    btnDownload = ttk.Button(root, text="Download", command=DownloadVideo(videoLink,selectedResolution))
    btnDownload.grid(row=10, column=0,sticky="ws")

Init()
#ytVideoLink = "https://www.youtube.com/watch?v=0qacFnuXSF8"
#DownloadVideo(ytVideoLink)