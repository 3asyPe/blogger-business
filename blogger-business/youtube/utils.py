from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build


API_ANALYTICS_SERVICE_NAME = "youtubeAnalytics"
API_ANALYTICS_VERSION = "v2"
API_DATA_SERVICE_NAME = "youtube"
API_DATA_VERSION = "v3"


def get_data_service(youtube):
    credentials = youtube.fetch_credentials()
    return build(API_DATA_SERVICE_NAME, API_DATA_VERSION, credentials=credentials)


def get_analytics_service(youtube):
    credentials = youtube.fetch_credentials()
    return build(API_ANALYTICS_SERVICE_NAME, API_ANALYTICS_VERSION, credentials=credentials)


def get_date_a_month_ago() -> date:
    month_ago = date.today() - relativedelta(months=1)
    return month_ago


def request_statistics_for_last_month(youtube):
    youtubeAnalytics = get_analytics_service(youtube)
    start_date = get_date_a_month_ago()
    start_date = start_date.replace(day=1)
    response = youtubeAnalytics.reports().query(   
        ids='channel==MINE',
        startDate=start_date,
        endDate=start_date,
        metrics='dislikes,views,likes,subscribersGained,comments',
        dimensions='month',
        sort='month',
    ).execute()
    print(response)
    return response


def request_total_statistics(youtube):
    dataApi = get_data_service(youtube)
    response = dataApi.channels().list(
        part="statistics",
        mine=True,
    ).execute()
    print(response)
    return response


def request_snippet_and_id_for_channel(youtube):
    dataApi = get_data_service(youtube)
    response = dataApi.channels().list(
        part="snippet",
        mine=True,
    ).execute()
    print(response)
    return response


def parse_month_statistics(response) -> dict:
    statistics = response["rows"][0]

    date_str = statistics[0]
    month = datetime.strptime(date_str, "%Y-%m").month
    dislikes = statistics[1]
    views = statistics[2]
    likes = statistics[3]
    subscribers_gained = statistics[4]
    comments = statistics[5]

    s_dict = {
        "month": month,
        "dislikes": dislikes,
        "likes": likes,
        "views": views,
        "subscribers_gained": subscribers_gained,
        "comments": comments
    }
    return s_dict


def parse_total_statistics(response) -> dict:
    statistics = response["items"][-1]["statistics"]

    s_dict = {
        "views": statistics["viewCount"],
        "subscribers": statistics["subscriberCount"],
        "video_count": statistics["videoCount"]
    }
    return s_dict


def parse_snippet_and_id(response) -> dict:
    snippet = response["items"][-1]["snippet"]
    channel_id = response["items"][-1]["id"]
    name = snippet["title"]
    
    s_dict = {
        "channel_id": channel_id,
        "name": name
    }
    return s_dict


def set_statistics_for_last_month(youtube_statistics, statistics):
    print(statistics)
    youtube_statistics.month_updated = statistics["month"]
    youtube_statistics.month_dislikes = statistics["dislikes"]
    youtube_statistics.month_likes = statistics["likes"]
    youtube_statistics.month_views = statistics["views"]
    youtube_statistics.month_subscribers_gained = statistics["subscribers_gained"]
    youtube_statistics.month_comments = statistics["comments"]
    youtube_statistics.save()
    return youtube_statistics


def set_total_statistics(youtube_statistics, statistics):
    print(statistics)
    youtube_statistics.total_views = statistics["views"]
    youtube_statistics.subscribers = statistics["subscribers"]
    youtube_statistics.total_video_count = statistics["video_count"]
    youtube_statistics.save()
    return youtube_statistics
