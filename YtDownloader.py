from pytube import YouTube
from pytube import Stream

#gui
ytVideoLink = "https://www.youtube.com/watch?v=0qacFnuXSF8"

def OnProgress(stream:Stream, chunk: bytes, bytes_remaining: int):
    totalfilesizeInKB = stream.filesize_kb*1000
    
    if(bytes_remaining == totalfilesizeInKB):
        print("Video found:{0} mb".format(stream.filesize_mb))
    
    if(bytes_remaining > 0):
        print("Progress: {0:0.2f}%".format(100-bytes_remaining/totalfilesizeInKB*100))
    
def OnDownloadComplete(arg1,arg2):
    print("Video downloaded!")

yt_instance = YouTube(ytVideoLink)
yt_instance.register_on_progress_callback(OnProgress)
yt_instance.register_on_complete_callback(OnDownloadComplete)

ytStream = yt_instance.streams.filter(file_extension="mp4").first()
ytVideo = ytStream.download(output_path="./yt_downloads")