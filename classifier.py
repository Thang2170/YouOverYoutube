import json
from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path
from google.genai import types
import ast

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

models = ['gemini-3.5-flash-lite','gemini-3.5-flash-lite','gemini-3.1-flash-lite','gemini-3.6-flash','gemini-3-flash-preview']

config = types.GenerateContentConfig(
    temperature=0,            
    max_output_tokens=500,     
)

key = os.getenv('GEMINI_API_KEY')
#print(key)
client = genai.Client(api_key=key)


def classify(video_id,banned_categories,user_keywords,debug=False):
    file_path = Path(f'video_data/{video_id}.json')
    with file_path.open('r', encoding='utf-8') as file:
        info = json.load(file)
    if info['response']['items'][0]['snippet']['categoryId'] in banned_categories:
        return {"allowed": False, "reason": "Violating Banned category"}
    else:
        if info['transcript'] == None:
            transcript = 'None'
        else:
            transcript = info['transcript'][:1500]
        title = info['response']['items'][0]['snippet']['title']
        description = info['response']['items'][0]['snippet']['description']
        if debug == True:
            print(info['response']['items'][0]['snippet']['tags'])
            return
        tags = ', '.join(info['response']['items'][0]['snippet'].get('tags', []))
        prompt = f" Only allowed Youtube videos according to the User Keywords: {user_keywords} and block the distracting, unrelated ones.The evidence: title {title}, description {description}, tags {tags}, transcript {transcript}. The output format is reply with only JSON, {{\"allowed\": True, \"reason\": \"...\"}}. reason 3-words short, fast. Edge-case guidance: “if unsure, not allowed,” “lofi study mixes is  music.” "
        #print(prompt)
        for i in range(len(models)):
            try:
                model_response = client.models.generate_content(
                model=models[i],
                contents=prompt,
                config = config
                )
                response_text = model_response.text.strip()
                if response_text.startswith("```"):
                    response_text = (response_text.
                                     removeprefix("```json").
                                     removesuffix("```").
                                     strip()
                    )
                    return json.loads(response_text)
            except Exception as error:
                print(f'Model {models[i]} failed: {error}')
                continue
        return {'allowed': True, "reason": "No current available models"}




    
if __name__ == "__main__":
    classify('iPaBw8FjqSM',['20'],'Music')