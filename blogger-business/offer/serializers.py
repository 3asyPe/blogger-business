from .models import Offer, ReceivingModel
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
