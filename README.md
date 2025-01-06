# Transcribe YouTube videos, even Live ones, into readable text.

Install:
```
pipx install insanely-fast-whisper
export PYTORCH_ENABLE_MPS_FALLBACK=1
pip install yt_dlp
```

## 1. Since insanely-fast-whisper only does audio; copy link to a youtube video into:
```
import os
from yt_dlp import YoutubeDL

def download_audio_from_youtube(url, output_path='output_audio.mp3'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    os.rename('temp_audio.mp3', output_path)
    return output_path

print("Downloading audio from YouTube...")
#              ****** COPY LINK HERE: *****************
youtube_url = "https://www.youtube.com/live/5Ov_D8DjBks"
#              ****************************************
audio_file_path = download_audio_from_youtube(youtube_url)
```
... run:
```
python -B cls_yt_audio.py
```


## 2. cls_yt_audio.py yields: audio.mp3 so then do:
```
insanely-fast-whisper --file-name output_audio.mp3 --device-id mps --model-name openai/whisper-large-v3 --batch-size 4
```
... 2 hours of audio takes about 12 minutes on a MacBook Pro M3 Max


## 3. step 3. yields: output.json so then do:
```
python -B convert_output.py output.json -f txt -o .
```
... see:
https://github.com/Vaibhavs10/insanely-fast-whisper/blob/main/convert_output.py


## 4. convert_output.py yields: output.txt so the last step is:
paragraphs, how?, so ChatGPT 4o gave me this:
```
python -B transcript_paragraphs.py 
```
... which uses output.txt to create formatted_output.txt (paragraphs)


## ... which is more readable, but not perfect, yet AI's can "read" it and summarize and give key takeaways

