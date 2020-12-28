import os

from BloggerBusiness.settings import secret


PATH_TO_CLIENT_SECRET = "BloggerBusiness/google_api/files/client_secret_76722557587-o7cb6jusf0ucadvfbb4g2vk5chn6nf3b.apps.googleusercontent.com.json"
SCOPES = [
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
]

CLIENT_ID = "76722557587-o7cb6jusf0ucadvfbb4g2vk5chn6nf3b.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", secret.GOOGLE_CLIENT_SECRET)
ACCESS_TYPE = 'offline'
INCLUDE_GRANTED_SCOPES = 'true'
LOGIN_HINT = "bloggerandbusiness@gmail.com"
 