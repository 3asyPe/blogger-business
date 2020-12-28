import requests
import httplib2

from django.conf import settings

import google_auth_oauthlib.flow
from googleapiclient.discovery import build

import oauth2client

from .models import Youtube


SCOPES = settings.GOOGLE_SCOPES

API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"
CLIENT_SECRET_FILE = settings.GOOGLE_PATH_TO_CLIENT_SECRET
CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
CLIENT_ID = settings.GOOGLE_CLIENT_ID


def create_youtube_model(blogger, code: str, name: str, email=None, image_url=None) -> Youtube:
    credentials = authorize_user(code=code)
    youtube = Youtube.objects.create(
        blogger=blogger,
        name=name,
        email=email,
        image_url=image_url,
        refresh_token=credentials.refresh_token,
        access_token=credentials.token,
        token_expires_in=3600,
    )
    return youtube


def request_statistics_for_last_month(youtube):
    youtubeAnalytics = _get_service(youtube)
    response = youtubeAnalytics.reports().query(   
        ids='channel==MINE',
        startDate='2020-01-01',
        endDate='2020-12-01',
        metrics='dislikes,views,likes,subscribersGained,comments',
        dimensions='month',
        sort='month',
    ).execute()
    print(response)


def authorize_user(code):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES
    )
    flow.redirect_uri = "postmessage"
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return credentials


def _get_service(youtube):
    credentials = youtube.fetch_credentials()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
