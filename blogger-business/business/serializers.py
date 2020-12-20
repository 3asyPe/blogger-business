import json

from .models import Business
from account.serializers import LocationSerializer
from emails.models import EmailActivation
from emails.serializers import UserProfileEmailActivationSerializer

from rest_framework import serializers


class BusinessSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    email_activation = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ['id', 'image', 'business_name', 'business_owner_name', 'email', 'phone', 'location', 'site', 'site', 'instagram', 'facebook', 'email_activation']
    
    def get_email_activation(self, obj):
        qs = EmailActivation.objects.confirmable().filter(user=obj.user)
        if not qs.exists():
            return None
        email_activation_obj = qs.last()
        serializer = UserProfileEmailActivationSerializer(email_activation_obj)
        return serializer.data


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
    email_activation = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ['email', 'phone', 'facebook', 'instagram', 'site', 'email_activation']

    def get_email_activation(self, obj):
        qs = EmailActivation.objects.confirmable().filter(user=obj.user)
        if not qs.exists():
            return None
        email_activation_obj = qs.last()
        serializer = UserProfileEmailActivationSerializer(email_activation_obj)
        return serializer.data
