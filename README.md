
### **overview**
a very simple python music sorter for music downloaded from youtube  
I use it for my small home file server, so it's tailored to that case   
it's not trying to be a "fit-all" solution

### **usage**
1. create folders with band names, it doesn't do that automatically (yet?)
2. just run and provide path to your music collection

or just put in the same folder with all the band folders for convenience (don't need a path then)

### **my yt-dlp config**
```config
# always extract audio
-x

# copy the mtime
--mtime

# write thumbnails as metadata
--embed-thumbnail

# wait between downloads to circumvent throttling
--sleep-interval 10

# proces videos in playlist as soon as they're received
--lazy-playlist

# retries (default 10)
--retries 3

# format filenames to minimalistic unix format
# this is needed for the script to run properly
--restrict-filenames
--no-windows-filenames

# save extracted audio in this directory
# replace PATH_TO_YOUR_MUSIC_FOLDER with your own path
# e.g. mine is ~/file-server/priv/music
-o PATH_TO_YOUR_MUSIC_FOLDER/%(title)s.%(ext)s
```
