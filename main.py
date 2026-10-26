from video_id import get_info_transcript
from classifier import classify
from pathlib import Path
video_id = '7Btm94g3T3Y'


if __name__ == "__main__":
    get_info_transcript(video_id)
    response = classify(video_id,['8'],'Discrete Math')
    print(type(response),response)