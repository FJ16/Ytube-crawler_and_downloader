# using youtube_dl template to download mp4 from youtube
import youtube_dl

# The youtube_dl provide an option to change the default download location
# Using 'outtmpl' : (project main path - this is not displayed) / new folder name /.../ %(title)s.%(ext)s
# %(title)s means the video original title, .%(ext)s means the video's default format
# youtube_dl build-in option to covert mp4 to mp3 file, also use Jason format to set attributes
# remember to add those (three) .exe files from transfer tool FFprobe software
ydl_opts = {'format': 'bestaudio/best','outtmpl': '/audio/%(title)s.%(ext)s','postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=FdXArRBjodY'])

