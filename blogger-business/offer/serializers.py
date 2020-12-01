from .models import (
    Offer, 
    ReceivingModel, 
    BloggerModel,
    BloggerModelLanguage,
    BloggerModelSpecialization,
    SubscribersNumberGroup,
)
from application.serializers import ApplicationSerializerForCount
from business.serializers import BusinessSerializer

from rest_framework import serializers


class ReceivingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivingModel
        fields = ['delivery', 'address']


class SubscribersNumberGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribersNumberGroup
        fields = ["group"]


class BloggerModelLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloggerModelLanguage
        fields = ["language"]


class BloggerModelSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloggerModelSpecialization
        fields = ["specialization"]


class BloggerModelSerializer(serializers.ModelSerializer):
    languages = BloggerModelLanguageSerializer(many=True)
    specializations = BloggerModelSpecializationSerializer(many=True)
    subscriber_groups = SubscribersNumberGroupSerializer(many=True)

    class Meta:
        model = BloggerModel
        fields = ["languages", "specializations", "subscriber_groups", "age_group", "sex"]


class OfferSerializer(serializers.ModelSerializer):
    business = BusinessSerializer()
    receiving_model = ReceivingModelSerializer()

    class Meta:
        model = Offer
        fields = ['id', 'business', 'image', 'title', 'description', 'conditions', 'price', 'receiving_model', 'validity']


class OfferEditViewSerializer(serializers.ModelSerializer):
    blogger_model = BloggerModelSerializer()
    
    class Meta:
        model = Offer
        fields = ['id', 'blogger_model', 'image', 'title', 'description', 'conditions', 'price', 'receiving_model', 'validity']


class OfferBusinessViewSerializer(serializers.ModelSerializer):
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'image', 'title', 'description', 'validity', 'applications_count']

    def get_applications_count(self, obj):
        return obj.application_set.count()
