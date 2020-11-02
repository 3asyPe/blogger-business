from rest_framework import serializers

from .models import Blogger


class BloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogger
        fields = ['id', 'image', 'blog_name', 'email', 'instagram', 'youtube', 'phone', 'location', 'sex', 'birthday']
