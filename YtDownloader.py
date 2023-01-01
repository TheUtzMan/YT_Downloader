from pytube import YouTube
from tkinter import Tk,Text,ttk
import json

class App:
    def __init__(self):
        """ Initializes the GUI for the application"""
        
        self.root = Tk()
        self.root.title("YouTube Downloader")
        self.root.geometry("640x480")
        self.root.resizable(False,False)
        self.root.config(bg="black")
        self.root.grid_rowconfigure(10, weight=1)

        ttk.Label(self.root, text="Enter a video link").grid(column=1, row=2,padx=20)
        self.video_link_text = Text(self.root, height=1, width=35)
        self.video_link_text.grid(column=1,row=3)
        self.video_link_text.bind("<KeyRelease>",self.SelectVideo)

        ttk.Button(self.root, text="Quit", command=self.root.destroy).grid(row=10,column=3,sticky="es")
        self.root.mainloop()

    def SelectVideo(self):
        self.videoLink = self.video_link_text.get("1.0",'end-1c')
        self.combobox = ttk.Combobox(self.root,textvariable="360p")
        self.combobox['values'] = ('144p', '240p', '360p', '480p', '720p', '1080p')
        self.combobox['state'] = 'readonly'
        self.combobox.bind("<<ComboboxSelected>>", self.SelectResolution)
        self.combobox.grid(column=2,row=3)

    def SelectResolution(self):
        self.selectedResolution = self.combobox.get()
        btnDownload = ttk.Button(self.root, text="Download", command=self.DownloadVideo)
        btnDownload.grid(row=10, column=0,sticky="ws")

    class AppSettings:
        def __init__(self):
            """ Initializes the GUI for the application settings"""
            pass
        
    class YTDownloader:  
        def __init__(self, **kwargs):
            """ Initializes the downloader with the provided url,resolution and output directory"""
            self.url = kwargs['url']
            self.resolution = kwargs['resolution']
            self.output_dir = kwargs['output_dir']

        def DownloadVideo(self):
            """ Tries downloading video with the initialized parameters. """
            try:
                yt_instance = YouTube(self.url)
                yt_instance.register_on_progress_callback(self.OnProgress)
                yt_instance.register_on_complete_callback(self.OnDownloadComplete)

                ytStream = yt_instance.streams.filter(file_extension="mp4",resolution=self.resolution).first()
                ytStream.download(output_path=self.output_dir)

            except Exception as e: print("Error: ",e)

        def OnProgress(stream, chunk, bytes_remaining):
            """ This event is fired at the beginning of a successful download 
                as well as during the whole process """
            bytes_downloaded = stream.filesize - bytes_remaining
            percentage_completion = bytes_downloaded/stream.filesize * 100
            
            if(bytes_remaining > 0):
                print("Progress: {0:0.1f}%".format(percentage_completion))

        def OnDownloadComplete(arg1,arg2):
            """ This event is fired when the download is completed"""
            print("Video downloaded!")