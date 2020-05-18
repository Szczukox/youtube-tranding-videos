import requests
import pandas as pd


def get_category_from_youtube_data_api(video_id):
    params = {
        "key": "AIzaSyB6pH3bqOztaQnc2hW39-MC8fDWlNvO2A0",
        "id": video_id,
        "part": "snippet"
    }

    try:
        response = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)
        if response.status_code == 200:
            video_content = response.json()["items"]
            if len(video_content) == 1:
                return int(video_content[0]["snippet"]["categoryId"])

        if response.status_code != 403:
            processed_trending.append(video_id)

        return "nan"
    except Exception:
        return "nan"


trending = pd.read_csv("trending.csv", sep=";")
trending = trending.loc[trending["category"].isna()]

processed_trending = pd.read_csv("processed_trending_ground_truth.csv", header=None)[0].to_list()

trending = trending.loc[~trending["video_id"].isin(processed_trending)]

trending["category"] = trending["video_id"].apply(get_category_from_youtube_data_api)

trending_with_category = pd.read_csv("trending_with_category.csv", sep=";")
trending_with_category = pd.concat([trending_with_category, trending])
trending_with_category.to_csv("trending_with_category.csv", index=False, sep=";")

pd.DataFrame({"video_id": processed_trending}).to_csv("processed_trending.csv", index=False, sep=";", header=None)
