from .models import Offer, ReceivingModel
from application.serializers import ApplicationSerializerForCount
from business.serializers import BusinessSerializer

from rest_framework import serializers


class ReceivingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivingModel
        fields = ['delivery', 'address']


class OfferSerializer(serializers.ModelSerializer):
    business = BusinessSerializer()
    receiving_model = ReceivingModelSerializer()

    class Meta:
        model = Offer
        fields = ['id', 'business', 'image', 'title', 'description', 'conditions', 'price', 'receiving_model', 'validity']


class OfferBusinessViewSerializer(serializers.ModelSerializer):
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'image', 'title', 'description', 'validity', 'applications_count']

    def get_applications_count(self, obj):
        return obj.application_set.count()
