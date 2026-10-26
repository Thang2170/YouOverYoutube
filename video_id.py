from googleapiclient.discovery import build
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv
import json
from pathlib import Path

ytt_api = YouTubeTranscriptApi()


load_dotenv()
api_key = os.getenv('my_api_key')
youtube = build('youtube','v3',developerKey= api_key)
def get_info_transcript(video_id):
    file_path = Path(f"video_data/{video_id}.json")
    if file_path.is_file():
        return video_id
    else:
        request = youtube.videos().list(
            part='snippet',
            id = video_id
        )
        response = request.execute()
        transcript = None
        try:
            transcript = ytt_api.fetch(video_id)
        except Exception as e:
            print(f"Couldn't download transcript for {video_id}: {e}")
        try:
            with open('data.json', 'r') as file:
                current_data = json.load(file)
        except FileNotFoundError:
            current_data = {}

        current_data['response'] = response
        if transcript is None:
            current_data['transcript'] = None
        else:
            current_data['transcript'] = ''.join(
                snippet.text for snippet in transcript
            )

        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w', encoding="utf-8") as file:
            json.dump(current_data,file,indent=4,ensure_ascii=False)
        return video_id




    
