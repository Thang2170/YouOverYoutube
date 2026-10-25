import json
from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

YOUTUBE_CATEGORIES = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "21": "Videoblogging",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
    "30": "Movies",
    "31": "Anime/Animation",
    "32": "Action/Adventure",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers",
}

key = os.getenv('GEMINI_API_KEY')
print(key)
client = genai.Client(api_key=key)

def classify(video_id,category):
    with open(f'{video_id}.json', 'r', encoding='utf-8') as file:
        info = json.load(file)
    if info['response']['items'][0]['snippet']['categoryId'] in category:
        return {"allowed": False, "reason": "Violating Banned category"}
    else:
        if info['transcript'] == None:
            return {"allowed": True, "reason": "Couldn't find transcript"}
        text = info['transcript'][:1500]
        print(text)




    
if __name__ == "__main__":
    classify('iPaBw8FjqSM',['20'])