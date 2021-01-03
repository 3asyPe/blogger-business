import oauth2client
import httplib2

from datetime import date
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from .utils import (
    request_statistics_for_last_month,
    request_total_statistics,
    request_snippet_and_id_for_channel,
    parse_month_statistics,
    parse_total_statistics,
    parse_snippet_and_id,
    set_statistics_for_last_month,
    set_total_statistics,
)
from blogger.models import Blogger


API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"
SCOPES = settings.GOOGLE_SCOPES
CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
CLIENT_ID = settings.GOOGLE_CLIENT_ID


class YoutubeManager(models.Manager):
    def create_new(self, blogger, name, email, image_url, credentials):
        youtube = self.model(
            blogger=blogger,
            name=name,
            email=email,
            image_url=image_url,
            refresh_token=credentials.refresh_token,
            access_token=credentials.token,
            token_expires_in=3600,
        )
        response = request_snippet_and_id_for_channel(youtube)
        s_dict = parse_snippet_and_id(response)
        youtube.name = s_dict["name"]
        youtube.channel_id = s_dict["channel_id"]
        youtube.save(using=self._db)
        return youtube


class Youtube(models.Model):
    blogger = models.OneToOneField(Blogger, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    refresh_token = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    updated_token = models.DateField()
    token_expires_in = models.IntegerField() 

    objects = YoutubeManager()

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
            access_token=None,
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

    def get_url(self):
        return f"https://www.youtube.com/channel/{self.channel_id}"

    def __str__(self):
        return self.name


class YoutubeStatisticsManager(models.Manager):
    def create_new(self, youtube):
        youtube_statistics = self.model(
            youtube=youtube,
        )
        youtube_statistics.udpate_statistics_for_last_month()
        youtube_statistics.update_total_statistics()
        youtube_statistics.save(using=self._db)
        return youtube_statistics


class YoutubeStatistics(models.Model):
    youtube = models.OneToOneField(Youtube, on_delete=models.CASCADE, related_name="statistics")

    subscribers = models.IntegerField(default=0)
    total_video_count = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    total_updated = models.DateTimeField(blank=True, null=True)

    month_views = models.IntegerField(default=0)
    month_comments = models.IntegerField(default=0)
    month_subscribers_gained = models.IntegerField(default=0)
    month_likes = models.IntegerField(default=0)
    month_dislikes = models.IntegerField(default=0)
    month_updated = models.IntegerField(blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)

    objects = YoutubeStatisticsManager()

    def udpate_statistics_for_last_month(self):
        response = request_statistics_for_last_month(self.youtube)
        statistics = parse_month_statistics(response)
        set_statistics_for_last_month(youtube_statistics=self, statistics=statistics)
        
    def update_total_statistics(self):
        response = request_total_statistics(self.youtube)
        statistics = parse_total_statistics(response)
        set_total_statistics(youtube_statistics=self, statistics=statistics)


def pre_save_youtube_change_token_receiver(sender, instance, *args, **kwargs):
    pre_instance_qs = sender.objects.filter(pk=instance.pk)
    if pre_instance_qs.exists():
        pre_instance = pre_instance_qs.first()
        if pre_instance.access_token == instance.access_token:
            return 

    instance.updated_token = timezone.now()


pre_save.connect(pre_save_youtube_change_token_receiver, sender=Youtube)


def pre_save_youtube_change_total_statistics_receiver(sender, instance, *args, **kwargs):
    pre_instance_qs = sender.objects.filter(pk=instance.pk)
    if pre_instance_qs.exists():
        pre_instance = pre_instance_qs.first()
        if pre_instance.subscribers == instance.subscribers and \
                pre_instance.total_video_count == instance.total_video_count and \
                pre_instance.total_views == instance.total_views:
            return 

    instance.total_updated = timezone.now()


pre_save.connect(pre_save_youtube_change_total_statistics_receiver, sender=YoutubeStatistics)
