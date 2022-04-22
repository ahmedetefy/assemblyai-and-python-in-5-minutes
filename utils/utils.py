import requests
import time
#import youtube_dl

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

# Create youtube_dl options dictionary
def _make_ydl_opts(ffmpeg_path):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "ffmpeg_location": ffmpeg_path,
        "outtmpl": "./%(id)s.%(ext)s",
    }
    return ydl_opts

# Download youtube video
def download_video(ffmpeg_path=".\\FFmpeg\\bin", yt_link='https://www.youtube.com/watch?v=x_406XLbjxY'):
	ydl_opts = make_ydl_opts(ffmpeg_path=ffmpeg_path)

	yt_link.strip()
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    meta = ydl.extract_info(yt_link)

	return meta

# Make header for AAI API
def make_header(api_key):
	header_auth_only = {"authorization": api_key}
	header = {
	    "authorization": api_key,
	    "content-type": "application/json"
	}
	return header

# Helper for `upload_file()`
def _read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

# Uploads a file to AAI servers
def upload_file(audio_file, header):
	upload_response = requests.post(
	    upload_endpoint,
	    header=header, data=_read_file(audio_file)
	)
	upload_url = upload_response.json()

	return upload_url

# Request transcript for file uploaded to AAI servers
def request_transcript(upload_url, header):
	transcript_request = {
    	'audio_url': upload_url['upload_url']
	}
	transcript_response = requests.post(transcript_endpoint, json=transcript_request, header=header)
	transcript_response = transcript_response.json()
	return transcript_response

# Make a polling endpoint
def make_polling_endpoint(transcript_response):
	polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
	polling_endpoint += transcript_response['id']
	return polling_endpoint

# Wait for the transcript to finish
def wait_for_completion(polling_endpoint, header):
	while True:
	    polling_response = requests.get(polling_endpoint, header=header)    
	    polling_response = polling_response.json()

	    if polling_response['status'] == 'completed':
	        break
	    
	    time.sleep(5)

# Get the paragraphs of the transcript
def get_paragraphs(polling_endpoint, header):
	paragraphs_response = requests.get(polling_endpoint + "/paragraphs", header=header)

	paragraphs = []
	paras = []
	for para in paragraphs_response.json()['paragraphs']:
	    paras.append(para)
	paragraphs.append(paras)

	return paras

