from pytube import YouTube
from tkinter import ttk
from threading import Thread

class YTDownloader:  
        """Class for downloading a video with the Pytube API"""
        def __init__(self, **kwargs):
            """ Initializes the downloader with the provided url,resolution and output directory"""
            self.url = kwargs['url']
            self.resolution = kwargs['resolution']
            self.output_dir = kwargs['output_dir']
            self.progressbar:ttk.Progressbar = kwargs['progressbar']
            global thread
            thread = Thread(target=self.download_video)
            thread.start()

        def download_video(self):
            """ Tries downloading video with the initialized parameters. """
            try:
                yt_instance = YouTube(self.url)
                yt_instance.register_on_progress_callback(self.on_progress)
                yt_instance.register_on_complete_callback(self.on_download_complete)

                ytStream = yt_instance.streams.filter (
                    file_extension="mp4",
                    resolution=self.resolution
                    ).first()
                
                self.title_label = ttk.Label(self.progressbar.master,text=ytStream.title)
                self.title_label.grid(column = 1, row = 4)
                self.progressbar.stop()
                self.progressbar["mode"] = "determinate"

                ytStream.download(output_path=self.output_dir)

            except Exception as e: print("Error: ",e)

        def on_progress(self,stream, chunk, bytes_remaining):
            """ This event is fired at the beginning of a successful download 
                as well as during the whole process """
            bytes_downloaded = stream.filesize - bytes_remaining
            percentage_completion = bytes_downloaded/stream.filesize * 100
            
            if(bytes_remaining > 0):
                #self.title_label["text"] = stream.
                self.progressbar["value"] = (percentage_completion)
                print(percentage_completion)

        def on_download_complete(self,stream,file_path):
            """ This event is fired when the download is completed"""
            self.progressbar["value"]=100
            self.title_label["text"] = ""
            self.title_label.grid()
            print("Finished")