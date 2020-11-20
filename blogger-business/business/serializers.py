from .models import Business
from account.serializers import LocationSerializer

from rest_framework import serializers


class BusinessSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Business
        fields = ['id', 'image', 'business_name', 'business_owner_name', 'email', 'phone', 'location', 'site', 'site', 'instagram', 'facebook']


class ImageInfoBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['image']


class BusinessInfoSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Business
        fields = ['business_name', 'business_owner_name', 'location']


class BusinessContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['email', 'phone', 'facebook', 'instagram', 'site']
