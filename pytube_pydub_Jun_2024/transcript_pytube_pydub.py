# pip install pytube pydub
import time
from pytube import YouTube
from pydub import AudioSegment
video_url = "https://www.youtube.com/live/04ubNY2w_uU?si=ei6wr-9avYk3dNAH"
start_time = time.time()
yt = YouTube(video_url)
audio_stream = yt.streams.filter(only_audio=True).first()
audio_file = audio_stream.download(filename='audio')
audio = AudioSegment.from_file(audio_file)
audio.export("audio.mp3", format="mp3")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Audio downloaded and converted to MP3 successfully in {elapsed_time:.2f} seconds!")
