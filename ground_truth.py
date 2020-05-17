import requests
import pandas as pd


def get_category_from_youtube_data_api(video_id):
    params = {
        "key": "AIzaSyAgTcCIXXsgffo8ApEk9Gdrxc3Z9QUuxyg",
        "id": video_id,
        "part": "snippet"
    }

    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)
    if response.status_code == 200:
        video_content = response.json()["items"]
        if len(video_content) == 1:
            return int(video_content[0]["snippet"]["categoryId"])

    return "nan"


trending = pd.read_csv("trending.csv", sep=";")
trending = trending.loc[trending["category"].isna()]
trending["category"] = trending['video_id'].apply(get_category_from_youtube_data_api)
trending.to_csv("trending_with_category.csv", index=False, sep=";")
