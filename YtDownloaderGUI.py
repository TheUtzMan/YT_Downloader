from tkinter import Tk,Text,ttk
from YTDownloader import YTDownloader
import json

class AppGUI:
    
    class AppSettings:
        def __init__(self):
            """ Initializes the GUI for the application settings"""
            self.file_directory = "./settings.json"
            pass
         
        def read_settings(self) -> bool :
            return False

        def write_settings(self):
            json.dumps(self.file_directory,obj="Saved settings directory")
            pass
        
        def edit_settings(self):
            pass

        def create_settings(self):
            pass

    def __init__(self):
        """ Initializes the GUI for the application"""
        
        self.root = Tk()
        self.root.title("YouTube Downloader")
        self.root.geometry("640x480")
        self.root.resizable(False,False)
        self.root.grid_rowconfigure(10, weight=1)

        ttk.Label(self.root, text="Enter a video link").grid(column=1, row=2,padx=20)
        self.video_link_text = Text(self.root, height=1, width=45)
        self.video_link_text.grid(column=1,row=3)
        self.video_link_text.bind("<KeyRelease>",self.select_video)

        ttk.Button(self.root, text="Quit", command=self.quit).grid(
            row=10,
            column=2,
            sticky="es"
            )
        self.application_settings = self.AppSettings()
        self.root.mainloop()

    def quit(self):
        self.application_settings.edit_settings()
        self.root.destroy()

    def select_video(self, video):
        global video_link
        video_link = self.video_link_text.get("1.0",'end-1c')

        if(video_link):    
            self.combobox = ttk.Combobox(self.root,textvariable="360p")
            self.combobox['values'] = ('144p', '240p', '360p', '480p', '720p', '1080p')
            self.combobox['state'] = 'readonly'
            self.combobox.bind("<<ComboboxSelected>>", self.select_resolution)
            self.combobox.grid(column=2,row=3)
            try: btnDownload.grid()
            except NameError: pass

    def select_resolution(self,arg1):
        global selected_resolution
        selected_resolution = self.combobox.get()
        global btnDownload
        btnDownload = ttk.Button(self.root, text="Download", command=self.start_download)
        btnDownload.grid(row=10, column=0,sticky="ws")

    def start_download(self):
        btnDownload.grid_forget()
        try:
            progressbar = ttk.Progressbar (
                self.root,
                orient="horizontal",
                length=300,
                mode="determinate"
                )
                
            progressbar.grid(column=0, row=6, columnspan=3, padx=200, pady=25)

            YTDownloader (
                url = video_link,
                resolution = selected_resolution, 
                output_dir = "./videos",
                progressbar = progressbar
            )
        
        except Exception as e:
                global error_label
                error_label = ttk.Label(self.root, text=e).grid(column=1, row=3)

application = AppGUI()