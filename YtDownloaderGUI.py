from tkinter import Tk,Text,ttk,Menu
from YTDownloader import YTDownloader
import json

class AppGUI:
    """Class for working with the application GUI"""

    class AppSettings:
        """Class for working with the application settings"""

        def __init__(self):
            """ Initializes the GUI for the application settings"""
            self.download_directory = "/output"
            self.read_settings()
            pass
         
        def read_settings(self) :
            """ Tries to read the settings of the application"""
            try:
                file = open("settings.json")
                self.download_directory = json.load(fp=file)
                print("Deserialized: {0}".format(self.download_directory))
                file.close()
            except FileNotFoundError :
                open("settings.json","x")
            except json.JSONDecodeError:
                #open("settings.json","r")
                pass

        def write_settings(self):
            """ Tries to save the settings of the application"""
            try:
                file = open("settings.json","w")
                json_string = json.dumps(self.download_directory,indent=4,separators=(". ","= "))
                file.write(json_string)
                print("Serialized: {0}".format(self.download_directory))
            except Exception as e :
                print("Could not write to settings.json\n{0}".format(e))
            finally: file.close() 

    def __init__(self):
        """ Initializes the GUI for the application"""
        
        self.root = Tk()
        self.root.title("YouTube Downloader")
        self.root.geometry("640x480")
        self.root.resizable(False,False)
        self.root.grid_rowconfigure(10, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(5, weight=1)

        ttk.Label(self.root, text="Enter a video link").grid(column=1, row=2,padx=20)
        self.video_link_text = Text(self.root, height=1, width=45)
        self.video_link_text.grid(column=1,row=3)
        self.video_link_text.bind("<KeyRelease>",self.select_video)

        ttk.Button(self.root, text="Quit", command=self.quit).grid(
            row=10,
            column=2,
            sticky="es"
            )

        menu = Menu(self.root)
        menu.add_command(label="Preferences",command=self.preferences_window)
        self.root.config(menu=menu)

        self.application_settings = self.AppSettings()
        self.root.mainloop()

    def save_settings(self,arg):
        """Overrides the settings for this application"""
        self.application_settings.download_directory = self.new_video_dir.get("1.0",'end-1c')

    def preferences_window(self):
        """Create a window for the application settings"""
        window = Tk()
        window.title("Preferences")
        window.geometry("320x240")
        window.resizable(False,False)
        ttk.Label(window, text="Enter a directory for the saved videos").grid(column=1, row=1,padx=20)
        
        self.new_video_dir = Text(window, height=1, width=39)
        self.new_video_dir.grid(column=1,row=2)
        self.new_video_dir.insert("1.0",self.application_settings.download_directory)
        self.new_video_dir.bind("<KeyRelease>",self.save_settings)
        window.mainloop()
        pass

    def quit(self):
        """Tries to save the application settings while quiting the application"""
        self.application_settings.write_settings()
        self.root.destroy()

    def select_video(self, video):
        """Processes the input for the video"""
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
        """Processes the input for the resolution of the video"""
        global selected_resolution
        selected_resolution = self.combobox.get()
        global btnDownload
        btnDownload = ttk.Button(self.root, text="Download", command=self.start_download)
        btnDownload.grid(row=10, column=0,sticky="ws")

    def start_download(self):
        """Tries to download the video with the provided input and filters"""
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
                output_dir = self.application_settings.download_directory,
                progressbar = progressbar
            )
        
        except Exception as e:
                global error_label
                error_label = ttk.Label(self.root, text=e).grid(column=1, row=3)

#Starts the program
application = AppGUI()