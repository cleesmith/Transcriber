# pip install pytube pydub

# import time
# from pytube import YouTube
# from pydub import AudioSegment
# video_url = "https://youtu.be/G9P4bLMi9UM?si=mPrfOI3eOk0RANme"
# start_time = time.time()
# yt = YouTube(video_url)
# # audio_stream = yt.streams.filter(only_audio=True).first()
# audio_stream = yt.streams
# audio_file = audio_stream.download(filename='audio')
# audio = AudioSegment.from_file(audio_file)
# audio.export("audio.mp3", format="mp3")
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Audio downloaded and converted to MP3 successfully in {elapsed_time:.2f} seconds!")


# from pytube import YouTube
# YouTube('https://youtu.be/G9P4bLMi9UM?si=mPrfOI3eOk0RANme').streams.first().download()
# yt = YouTube('https://youtu.be/G9P4bLMi9UM?si=mPrfOI3eOk0RANme')
# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

