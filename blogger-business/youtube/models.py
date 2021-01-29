import oauth2client
import httplib2

from datetime import date
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

from .utils import (
    request_statistics_for_last_month,
    request_total_statistics,
    request_snippet_and_id_for_channel,
    request_audience_info,
    parse_month_statistics,
    parse_total_statistics,
    parse_snippet_and_id,
    parse_audience_info,
    set_statistics_for_last_month,
    set_total_statistics,
    set_refreshed_channel_info,
    set_audience_info,
)
from blogger.models import Blogger


API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"
SCOPES = settings.GOOGLE_SCOPES
CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
CLIENT_ID = settings.GOOGLE_CLIENT_ID

AGE_GROUPS = settings.AGE_GROUPS
SEXES = settings.SEXES


class YoutubeQuerySet(models.query.QuerySet):
    def get_active_ids(self):
        return self.filter(is_active=True).values_list('id', flat=True)

    def get_active_accounts(self):
        return self.filter(is_active=True)


class YoutubeManager(models.Manager):
    def get_queryset(self):
        return YoutubeQuerySet(self.model, self._db)

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
        if s_dict is not None:
            set_refreshed_channel_info(youtube=youtube, info=s_dict)
        youtube.save(using=self._db)
        return youtube

    def get_active_ids(self):
        return self.get_queryset().get_active_ids()

    def get_active_accounts(self):
        return self.get_queryset().get_active_accounts()


class Youtube(models.Model):
    blogger = models.OneToOneField(Blogger, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    refresh_token = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    updated_token = models.DateTimeField()
    token_expires_in = models.IntegerField() 
    published_at = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

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

    def refresh_channel_info(self) -> bool:
        response = request_snippet_and_id_for_channel(self)
        s_dict = parse_snippet_and_id(response)
        if s_dict is not None:
            if self.channel_id is None:
                YoutubeStatistics.objects.create_new(youtube=self)
            else:
                self.statistics.update_total_statistics()
                self.statistics.update_statistics_for_last_month()
            set_refreshed_channel_info(youtube=self, info=s_dict)
            return True
        return False

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
        if not self.channel_id:
            return None
        return f"https://www.youtube.com/channel/{self.channel_id}"

    def __str__(self):
        return self.name


class YoutubeStatisticsManager(models.Manager):
    def create_new(self, youtube):
        youtube_statistics = self.model(
            youtube=youtube,
        )
        youtube_statistics.update_statistics_for_last_month()
        youtube_statistics.update_total_statistics()
        youtube_statistics.save(using=self._db)
        return youtube_statistics


class YoutubeStatistics(models.Model):
    youtube = models.OneToOneField(Youtube, on_delete=models.CASCADE, related_name="statistics")

    subscribers = models.IntegerField(default=0)
    total_video_count = models.IntegerField(default=0)
    total_views = models.BigIntegerField(default=0)
    total_updated = models.DateTimeField(blank=True, null=True)

    month_views = models.BigIntegerField(default=0)
    month_comments = models.IntegerField(default=0)
    month_subscribers_gained = models.IntegerField(default=0)
    month_likes = models.IntegerField(default=0)
    month_dislikes = models.IntegerField(default=0)
    month_updated = models.IntegerField(blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)

    objects = YoutubeStatisticsManager()

    def update_statistics_for_last_month(self):
        response = request_statistics_for_last_month(self.youtube)
        statistics = parse_month_statistics(response)
        set_statistics_for_last_month(youtube_statistics=self, statistics=statistics)
        
    def update_total_statistics(self):
        response = request_total_statistics(self.youtube)
        statistics = parse_total_statistics(response)
        set_total_statistics(youtube_statistics=self, statistics=statistics)

    def __str__(self):
        return self.youtube.name


class YoutubeAudienceManager(models.Manager):
    def create_new(self, youtube: Youtube):
        youtube_audience = self.model(
            youtube=youtube
        )
        youtube_audience.update_info()
        youtube_audience.save(using=self._db)
        return youtube_audience


class YoutubeAudience(models.Model):
    youtube = models.OneToOneField(Youtube, on_delete=models.CASCADE, related_name="audience")
    age_group = models.CharField(max_length=50, default="18-24")
    sex = models.CharField(max_length=1, choices=SEXES, default="M")

    updated = models.DateTimeField(auto_now=True)

    objects = YoutubeAudienceManager()

    def update_info(self):
        response = request_audience_info(youtube=self.youtube)
        s_dict = parse_audience_info(response=response)
        set_audience_info(youtube_audience=self, info=s_dict)

    def __str__(self):
        return self.youtube.name


def post_save_youtube_is_active_check(sender, instance, *args, **kwargs):
    if instance.channel_id and hasattr(instance, "statistics") and not instance.is_active:
        instance.is_active = True
        instance.save()
    elif (not instance.channel_id or not hasattr(instance, "statistics")) and instance.is_active:
        instance.is_active = False
        instance.save()


post_save.connect(post_save_youtube_is_active_check, sender=Youtube)


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
