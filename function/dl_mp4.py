# using youtube_dl template to download mp4 from youtube
import youtube_dl

# The youtube_dl provide an option to change the default download location
# Using 'outtmpl' : (project main path - this is not displayed) / new folder name /.../ %(title)s.%(ext)s
# %(title)s means the video original title, .%(ext)s means the video's default format
ydl_opts = {'format': 'best','outtmpl': '/video/%(title)s.%(ext)s'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=FdXArRBjodY'])