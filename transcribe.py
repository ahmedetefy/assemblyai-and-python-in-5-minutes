from utils.utils import *
import sys

if len(sys.argv) == 3:
	api_key = sys.argv[2]
	audio_file = sys.argv[1]
else:
	api_key = "<YOUR-API-KEY>"
	audio_file = "audio.mp3"
	#audio_file = "https://github.com/AssemblyAI-Examples/speech-recognition-in-5-minutes-with-python/raw/main/audio.mp3"

# Whether or not the file is local
local = True


# Create header with authorization along with AssemblyAI API requests
header = make_header(api_key)

if local:
	# Upload the audio file to AssemblyAI
	upload_url = upload_file(audio_file, header)
else:
	upload_url = {'upload_url': audio_file}
	
# Request a transcription
transcript_response = request_transcript(upload_url, header)

# Create a polling endpoint that will let us check when the transcription is complete
polling_endpoint = make_polling_endpoint(transcript_response)

# Wait until the transcription is complete
wait_for_completion(polling_endpoint, header)

# Request the paragraphs of the transcript
paras = get_paragraphs(polling_endpoint, header)

# Save and print transcript
with open('transcript.txt', 'w') as f:
	for para in paras:
    		print(para['text'], '\n')
    		f.write(para['text'] + '\n')
