# *****************************************************
# often you see 403 Forbidden and the fix is to update:
#   pip install -U yt-dlp
# * don't forget about: ffmpeg and ffprobe too
# *****************************************************
import os
import argparse
import subprocess
import json
import re
import textwrap

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

def transcribe_audio():
	command = [
		"insanely-fast-whisper",
		"--file-name", "output_audio.mp3",
		"--device-id", "mps",
		"--model-name", "openai/whisper-large-v3",
		"--batch-size", "4"
	]
	try:
		subprocess.run(command, check=True)
	except subprocess.CalledProcessError as e:
		print(f"transcribe_audio: an error occurred during transcription: {e}")
		raise  # re-raise the exception to stop execution


class TxtFormatter:
    @classmethod
    def preamble(cls):
        return ""

    @classmethod
    def format_chunk(cls, chunk, index):
        text = chunk['text']
        return f"{text}\n"


class SrtFormatter:
    @classmethod
    def preamble(cls):
        return ""

    @classmethod
    def format_seconds(cls, seconds):
        whole_seconds = int(seconds)
        milliseconds = int((seconds - whole_seconds) * 1000)
        hours = whole_seconds // 3600
        minutes = (whole_seconds % 3600) // 60
        seconds = whole_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    @classmethod
    def format_chunk(cls, chunk, index):
        text = chunk['text']
        start, end = chunk['timestamp'][0], chunk['timestamp'][1]
        start_format, end_format = cls.format_seconds(start), cls.format_seconds(end)
        return f"{index}\n{start_format} --> {end_format}\n{text}\n\n"


class VttFormatter:
    @classmethod
    def preamble(cls):
        return "WEBVTT\n\n"

    @classmethod
    def format_seconds(cls, seconds):
        whole_seconds = int(seconds)
        milliseconds = int((seconds - whole_seconds) * 1000)
        hours = whole_seconds // 3600
        minutes = (whole_seconds % 3600) // 60
        seconds = whole_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    @classmethod
    def format_chunk(cls, chunk, index):
        text = chunk['text']
        start, end = chunk['timestamp'][0], chunk['timestamp'][1]
        start_format, end_format = cls.format_seconds(start), cls.format_seconds(end)
        return f"{index}\n{start_format} --> {end_format}\n{text}\n\n"

def convert(input_path, output_format, output_dir):
    with open(input_path, 'r') as file:
        data = json.load(file)
    formatter_class = {
        'srt': SrtFormatter,
        'vtt': VttFormatter,
        'txt': TxtFormatter
    }.get(output_format)

    string = formatter_class.preamble()
    for index, chunk in enumerate(data['chunks'], 1):
        entry = formatter_class.format_chunk(chunk, index)
        # if verbose:
        #     print(entry)
        string += entry
    with open(os.path.join(output_dir, f"output.{output_format}"), 'w', encoding='utf-8') as file:
        file.write(string)

def add_paragraphs(transcribed_text, sentences_per_paragraph=5, line_width=70):
    # normalize spaces
    transcribed_text = re.sub(r'\s+', ' ', transcribed_text).strip()
    
    # split the text into sentences, keeping the punctuation with the sentence
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
    sentences = sentence_endings.split(transcribed_text)

    paragraphs = []
    for i in range(0, len(sentences), sentences_per_paragraph):
        paragraph = ' '.join(sentences[i:i + sentences_per_paragraph]).strip()
        wrapped_paragraph = textwrap.fill(paragraph, width=line_width)
        paragraphs.append(wrapped_paragraph)

    formatted_text = '\n\n'.join(paragraphs)

    # ensure the last sentence has punctuation
    if not re.search(r'[.!?]$', formatted_text.strip()):
        formatted_text += '.'

    return formatted_text


def main():
	try:
		parser = argparse.ArgumentParser(description="Download audio from a YouTube video.")
		parser.add_argument('url', type=str, help="YouTube video URL")
		parser.add_argument('-o', '--output', type=str, default='output_audio.mp3', help="Output file name (default: output_audio.mp3)")
		args = parser.parse_args()
		# python -B cls_yt_audio.py https://www.youtube.com/live/0LWMNBauqHA
		print("Downloading audio from YouTube...")
		try:
			audio_file_path = download_audio_from_youtube(args.url, args.output)
			print(f"Audio downloaded successfully and saved to {audio_file_path}\n")
		except Exception as e:
			print(f"An error occurred: {e}\n")

		# insanely-fast-whisper --file-name output_audio.mp3 --device-id mps --model-name openai/whisper-large-v3 --batch-size 4
		print("Transcribing audio...")
		transcribe_audio()
		print("Transcription completed successfully.\n")
	except subprocess.CalledProcessError as e:
		print(f"Error: A command failed with exit code {e.returncode}. Details: {e}")
		print("Aborting operation.\n")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")
		print("Aborting operation.\n")

	# python -B convert_output.py output.json -f txt -o .
	convert("output.json", "txt", ".")
	print(f"Converted output.json to output.txt\n")

	# python -B transcript_paragraphs.py
	with open('output.txt', 'r') as file:
	    transcribed_text = file.read()
	formatted_text = add_paragraphs(transcribed_text, sentences_per_paragraph=3, line_width=70)
	with open('output_formatted.txt', 'w') as file:
	    file.write(formatted_text)
	print("Formatted text with paragraphs and line wrapping has been saved to 'output_formatted.txt'.")


if __name__ == "__main__":
	main()

