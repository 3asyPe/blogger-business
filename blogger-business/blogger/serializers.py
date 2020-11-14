from django.conf import settings

from .models import Blogger, BlogSpecialization, BlogLanguage
from account.serializers import LocationSerializer

from rest_framework import serializers


BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS


class BlogSpecializationSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source="get_specialization_display")

    class Meta:
        model = BlogSpecialization
        fields = ["specialization"]


class BlogLanguageSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source="get_language_display")

    class Meta:
        model = BlogLanguage
        fields = ["language"]


class BloggerSerializer(serializers.ModelSerializer):
    specializations = BlogSpecializationSerializer(many=True)
    languages = BlogLanguageSerializer(many=True)
    location = LocationSerializer()

    class Meta:
        model = Blogger
        fields = ['image', 'blog_name', 'email', 'instagram', 'youtube', 'phone', 'location', 'sex', 'birthday', 'specializations', 'languages', 'location']
