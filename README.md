# Transcribe any YouTube video into readable text <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;even Live ones or Short ones

> Please note youtube's rules and regulations, of course.

> Not everyone benefits from, nor enjoys such *eye candy* as, giant talking heads with background music trying to influence us, we prefer our propaganda in words ---the old fashion way.<br>Well, some of us. 🙋🏽‍♂️

---

Install:
```
pipx install insanely-fast-whisper
export PYTORCH_ENABLE_MPS_FALLBACK=1
pip install yt_dlp
```
### Now, go research: *ffmpeg* and *ffprobe* to get those installed too.

---

# Transcribe a video all in-one-go:
clean up any previous stuff:
```
rm output*
```
note the following may run for a while: 
> like on a macbook pro m3 max, a 1.5 hour video takes about 17 minutes; so pack a lunch as 'insanely-fast' is a bit slow and may lead to insanity

```
python -B transcriber.py https://youtube.com/shorts/kqIjyGQNGaU 
```

---

# Or transcribe a video in multiple steps:
> coz it's the journey, not the destination; right?

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
rm output*
```
```
python -B cls_yt_audio.py
```

## 2. cls_yt_audio.py yields: audio.mp3 so then do:
```
insanely-fast-whisper ---file-name output_audio.mp3 ---device-id mps ---model-name openai/whisper-large-v3 ---batch-size 4
```
> get coffee, walk the dog, mow the yard, sweep up around the ashram; kill time ⏳

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
... which uses output.txt to create output_formatted.txt (paragraphs)

### ... which is more readable, but not perfect, yet AI's can "read" it and summarize and give key takeaways
> and the opposite of giant talking heads rambling on and on 🤓

---

> Here's hoping that someday YouTube will wake up and smell the AI, embrace the qubits, then offer something like this process as a part of their service.

---


