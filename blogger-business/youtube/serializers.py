from rest_framework import serializers

from .models import Youtube, YoutubeStatistics


class YoutubeStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeStatistics
        fields = ['subscribers', 'total_video_count', 'total_views', 'total_updated',
                  'month_views', 'month_comments', 'month_subscribers_gained', 'month_likes',
                  'month_dislikes', 'month_updated', 'updated']


class YoutubeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    statistics = YoutubeStatisticsSerializer()

    class Meta:
        model = Youtube
        fields = ['channel_id', 'name', 'email', 'image_url', 'url', 'statistics']

    def get_url(self, obj):
        return obj.get_url()
