from googleapiclient.discovery import build
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv
import json

ytt_api = YouTubeTranscriptApi()


load_dotenv()
api_key = os.getenv('my_api_key')
youtube = build('youtube','v3',developerKey= api_key)
def get_info_transcript(video_id):
    request = youtube.videos().list(
        part='snippet',
        id = video_id
    )
    response = request.execute()
    try:
        transcript = ytt_api.fetch(video_id)
    except Exception as e:
        print(f'Couldnt download transcritp: {e}')
    try:
        with open('data.json', 'r') as file:
            current_data = json.load(file)
    except FileNotFoundError:
        current_data = {}

    current_data['response'] = response
    full_text_transcript = ''
    for snippet in transcript:
        full_text_transcript = full_text_transcript+ snippet.text
    current_data['transcript'] = full_text_transcript
    with open(f'{video_id}.json','w') as file:
        json.dump(current_data,file,indent=4)
    return




    
