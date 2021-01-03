from django.conf import settings

from .models import Blogger, BlogSpecialization, BlogLanguage
from account.serializers import LocationSerializer
from emails.models import EmailActivation
from emails.serializers import UserProfileEmailActivationSerializer
from youtube.serializers import YoutubeSerializer

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
    email_activation = serializers.SerializerMethodField()
    youtube = YoutubeSerializer()

    class Meta:
        model = Blogger
        fields = ['id', 'image', 'blog_name', 'email', 'instagram', 'youtube', 'phone', 'location', 'sex', 'birthday', 'specializations', 'languages', 'location', 'email_activation']

    def get_email_activation(self, obj):
        qs = EmailActivation.objects.confirmable().filter(user=obj.user)
        if not qs.exists():
            return None
        email_activation_obj = qs.last()
        if obj.user.email == email_activation_obj.email:
            return None
        serializer = UserProfileEmailActivationSerializer(email_activation_obj)
        return serializer.data


class ImageInfoBloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogger
        fields = ['image']


class PersonalInfoBloggerSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Blogger
        fields = ['blog_name', 'location', 'birthday']


class BlogInfoBloggerSerializer(serializers.ModelSerializer):
    languages = BlogLanguageSerializer(many=True)
    specializations = BlogSpecializationSerializer(many=True)
    email_activation = serializers.SerializerMethodField()

    class Meta:
        model = Blogger
        fields = ['languages', 'specializations', 'phone', 'email', 'email_activation']

    def get_email_activation(self, obj):
        qs = EmailActivation.objects.confirmable().filter(user=obj.user)
        if not qs.exists():
            return None
        email_activation_obj = qs.last()
        serializer = UserProfileEmailActivationSerializer(email_activation_obj)
        return serializer.data
