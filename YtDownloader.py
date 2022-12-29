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

def DownloadVideo(video_link:str):
    yt_instance = YouTube(video_link)
    yt_instance.register_on_progress_callback(OnProgress)
    yt_instance.register_on_complete_callback(OnDownloadComplete)

    ytStream = yt_instance.streams.filter(file_extension="mp4").first()
    ytStream.download(output_path="./yt_downloads")

def Init():
    root = Tk()
    root.resizable(width=False,height=False)
    root.title("YouTube Downloader")
    root.geometry("500x500")
    root.config(bg="black")

    frm = ttk.Frame(root)
    frm.grid()

    ttk.Label(frm, text="Enter a video link").grid(column=1, row=2,padx=20)
    video_link_text = Text(frm, height=1, width=35)
    video_link_text.grid(column=2,row=2)

    combobox = ttk.Combobox(frm,textvariable="360p")
    combobox['values'] = ('180p', '240p', '360p', '480p', '720p', '1080p')
    combobox['state'] = 'readonly'
    combobox.bind('<<ComboboxSelected>>', SelectResolution(combobox.get()))

    #btnDownload = ttk.Button(frm, text="Download", command=DownloadVideo(video_link_text.get("1.0",END)))
    #btnDownload.grid(column=0, row=1)
    #add button when stopped writing and input is a link
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=3)

    root.mainloop()

def SelectResolution(resolution:str):
    selectedResolution = resolution
    

Init()
#ytVideoLink = "https://www.youtube.com/watch?v=0qacFnuXSF8"
#DownloadVideo(ytVideoLink)