from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from blogger.models import Blogger


API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"
SCOPES = settings.GOOGLE_SCOPES
CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
CLIENT_ID = settings.GOOGLE_CLIENT_ID


class Youtube(models.Model):
    blogger = models.OneToOneField(Blogger, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    refresh_token = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    updated_token = models.DateField()
    token_expires_in = models.IntegerField() 

    def access_token_is_active(self):
        now = timezone.now()
        end_range = self.updated_token + timedelta(seconds=self.token_expires_in)
        if now < end_range:
            return True
        return False 

    def get_access_token(self):
        if not self.access_token_is_active:
            self.refresh_token()
        return self.refresh_access_token

    def refresh_access_token(self):
        credentials = self.fetch_credentials()
        self.access_token = credentials.access_token
        self.token_expires_in = credentials.expires_in
        self.save()

    def fetch_credentials(self):
        credentials = oauth2client.client.GoogleCredentials(
            access_token=self.access_token,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=self.refresh_token,
            token_expiry=None,
            token_uri=oauth2client.GOOGLE_TOKEN_URI,
            user_agent=None,
            revoke_uri=oauth2client.GOOGLE_REVOKE_URI
        )
        http = credentials.authorize(httplib2.Http())
        credentials.refresh(http)
        return credentials

    def __str__(self):
        return self.name


class YoutubeMonthStatistics(models.Model):
    youtube = models.OneToOneField(Youtube, on_delete=models.CASCADE, related_name="statistics")
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    comments = models.IntegerField()
    subscribers_gained = models.IntegerField()
    views = models.IntegerField()
    updated = models.DateTimeField(auto_now_add=True)


def pre_save_youtube_change_token_receiver(sender, instance, *args, **kwargs):
    pre_instance_qs = sender.objects.filter(pk=instance.pk)
    if pre_instance_qs.exists():
        pre_instance = pre_instance_qs.first()
        if pre_instance.access_token == instance.access_token:
            return 

    instance.updated_token = timezone.now()


pre_save.connect(pre_save_youtube_change_token_receiver, sender=Youtube)
