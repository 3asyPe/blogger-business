import google_auth_oauthlib.flow
import requests
import httplib2
import oauth2client

from django.conf import settings

from .models import Youtube, YoutubeStatistics


SCOPES = settings.GOOGLE_SCOPES


CLIENT_SECRET_FILE = settings.GOOGLE_PATH_TO_CLIENT_SECRET
CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
CLIENT_ID = settings.GOOGLE_CLIENT_ID


def create_youtube_model(blogger, code: str, name: str, email=None, image_url=None) -> Youtube:
    credentials = authorize_user(code=code)
    youtube = Youtube.objects.create_new(
        blogger=blogger,
        name=name,
        email=email,
        image_url=image_url,
        credentials=credentials
    )
    youtube_statistics = create_youtube_statistics_model(youtube)
    return youtube


def create_youtube_statistics_model(youtube: Youtube) -> YoutubeStatistics:
    youtube_statistics = YoutubeStatistics.objects.create_new(youtube=youtube)
    return youtube_statistics

def authorize_user(code):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES
    )
    flow.redirect_uri = "postmessage"
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return credentials