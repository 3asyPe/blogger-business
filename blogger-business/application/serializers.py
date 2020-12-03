from rest_framework import serializers

from .models import Application
from blogger.serializers import BloggerSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    blogger = BloggerSerializer()

    class Meta:
        model = Application
        fields = ['id', 'blogger', 'timestamp']


class ApplicationSerializerForCount(serializers.ModelSerializer):
    class Meta:
        fields = ['id']
