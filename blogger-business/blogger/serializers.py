from rest_framework import serializers

from .models import Blogger


class BloggerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogger
        fields = ['image', 'blog_name', 'email', 'phone', 'sex']
