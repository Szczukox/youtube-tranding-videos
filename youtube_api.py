import requests
import pandas as pd

is_403 = False


def search_related_video_id_from_youtube_data_api(video_id):
    params = {
        "key": "AIzaSyB6pH3bqOztaQnc2hW39-MC8fDWlNvO2A0",
        "maxResults": 50,
        "order": "relevance",
        "part": "id",
        "publishedAfter": "2017-11-14T00:00:00Z",
        "publishedBefore": "2018-06-14T00:00:00Z",
        "relatedToVideoId": video_id,
        "type": "video"
    }

    response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
    videos = []
    if response.status_code == 200:
        for item in response.json()["items"]:
            videos.append(item["id"]["videoId"])

    global is_403
    if response.status_code != 403:
        processed_trending.append(video_id)
    else:
        is_403 = True
    return videos


def find_videos_content_by_ids_from_youtube_data_api(video_ids):
    video_data = {}
    params = {
        "key": "AIzaSyB6pH3bqOztaQnc2hW39-MC8fDWlNvO2A0",
        "id": ','.join(video_ids),
        "part": "id,snippet,statistics"
    }

    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)
    if response.status_code == 200:
        for item in response.json()["items"]:
            video_data[item["id"]] = item

    return video_data


def map_video_content_to_data_frame_series(video_data, non_trending):
    for video_content in video_data.values():
        video_id = video_content["id"]

        snippet = video_content["snippet"]
        title = snippet.get("title", "")
        channel_title = snippet.get("channelTitle", "")
        category_id = int(snippet.get("categoryId", ""))
        publish_time = snippet["publishedAt"]
        tags = snippet.get("tags", [])
        thumbnail_link = snippet["thumbnails"]["default"]["url"]
        description = snippet.get("description", "")

        statistics = video_content["statistics"]
        views = statistics.get("viewCount", 0)
        likes = statistics.get("likeCount", 0)
        dislikes = statistics.get("dislikeCount", 0)
        comment_count = statistics.get("commentCount", 0)

        if likes == 0 and dislikes == 0:
            ratings_disabled = True
        else:
            ratings_disabled = False

        if comment_count == 0:
            comments_disabled = True
        else:
            comments_disabled = False

        series = pd.Series(
            [video_id, title, channel_title, category_id, publish_time, tags, views, likes, dislikes, comment_count,
             thumbnail_link, comments_disabled, ratings_disabled, description], index=non_trending.columns)
        non_trending = non_trending.append(series, ignore_index=True)

    return non_trending


trending = pd.read_csv("trending.csv", sep=";")
processed_trending = pd.read_csv("processed_trending.csv", header=None)[0].to_list()
trending = trending.loc[~trending["video_id"].isin(processed_trending)]
trending_video_ids = trending["video_id"].to_list()

non_trending = pd.read_csv("video_from_youtube_data_api.csv", sep=";")

for trending_video_id in trending_video_ids:
    related_video_ids = search_related_video_id_from_youtube_data_api(trending_video_id)
    non_trending_video_ids = [related_video_id for related_video_id in related_video_ids if
                              related_video_id not in trending_video_ids]
    video_data = find_videos_content_by_ids_from_youtube_data_api(non_trending_video_ids)
    non_trending = map_video_content_to_data_frame_series(video_data, non_trending)
    if is_403:
        break

non_trending["publish_time"] = non_trending["publish_time"].map(
    lambda publish_time: pd.Timestamp(pd.Timestamp(publish_time).date()))

min_trending_date = pd.Timestamp(trending["first_trending_date"].min())
max_trending_date = pd.Timestamp(trending["first_trending_date"].max())

non_trending = non_trending.loc[
    (non_trending["publish_time"] > min_trending_date) & (non_trending["publish_time"] < max_trending_date)]

pd.DataFrame({"video_id": processed_trending}).to_csv("processed_trending.csv", index=False, sep=";", header=None)
non_trending.drop_duplicates(subset=["video_id"])
non_trending.to_csv("video_from_youtube_data_api.csv", index=False, sep=";")
