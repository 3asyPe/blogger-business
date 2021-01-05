from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
from typing import Optional

from BloggerBusiness.utils import parse_isoformat_time

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
        metrics='dislikes,likes,views,subscribersGained,comments',
        dimensions='month',
        sort='month'
    ).execute()
    print(response)
    return response


def request_total_statistics(youtube):
    data_api = get_data_service(youtube)
    response = data_api.channels().list(
        part="statistics",
        mine=True,
    ).execute()
    print(response)
    return response


def request_snippet_and_id_for_channel(youtube):
    data_api = get_data_service(youtube)
    response = data_api.channels().list(
        part="snippet",
        mine=True,
    ).execute()
    print(response)
    return response


def request_audience_info(youtube):
    youtubeAnalytics = get_analytics_service(youtube)
    start_date = youtube.published_at.strftime("%Y-%m-%d")
    end_date = date.today()
    response = youtubeAnalytics.reports().query(   
        ids='channel==MINE',
        startDate=start_date,
        endDate=end_date,
        metrics='viewerPercentage',
        dimensions='ageGroup,gender',
        sort='gender,ageGroup',
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


def parse_total_statistics(response) -> Optional[dict]:
    ''' Response doesn't have items if youtube account doesn't exist.
    It might happen if user have a google account but doesn't have a youtube
    '''
    try:
        statistics = response["items"][-1]["statistics"]
    except KeyError:
        return None

    s_dict = {
        "views": statistics["viewCount"],
        "subscribers": statistics["subscriberCount"],
        "video_count": statistics["videoCount"]
    }
    return s_dict


def parse_snippet_and_id(response) -> Optional[dict]:
    ''' Response doesn't have items if youtube account doesn't exist.
    It might happen if user have a google account but doesn't have a youtube
    '''
    try:
        snippet = response["items"][-1]["snippet"]
    except KeyError:
        return None
    channel_id = response["items"][-1]["id"]
    name = snippet["title"]
    published_at = parse_isoformat_time(snippet["publishedAt"])
    
    s_dict = {
        "channel_id": channel_id,
        "name": name,
        "published_at": published_at,
    }
    return s_dict


def parse_audience_info(response) -> dict:
    info = response["rows"][0]

    age_group = _parse_response_age_group(info[0])
    sex = _parse_response_gender(info[1])

    s_dict = {
        "age_group": age_group,
        "sex": sex,
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


def set_refreshed_channel_info(youtube, info):
    youtube.name = info["name"]
    youtube.channel_id = info["channel_id"]
    youtube.published_at = info["published_at"]
    youtube.save()
    return youtube


def set_audience_info(youtube_audience, info):
    print(info)
    youtube_audience.age_group = info["age_group"]
    youtube_audience.sex = info["sex"]
    youtube_audience.save()
    return youtube_audience


def _parse_response_age_group(r_age_group: str) -> str:
    return r_age_group.replace("age", "")


def _parse_response_gender(r_gender: str) -> str:
    if r_gender == "male":
        return "M"
    else:
        return "W"
