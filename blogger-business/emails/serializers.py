from .models import EmailActivation 

from rest_framework import serializers


class UserProfileEmailActivationSerializer(serializers.ModelSerializer):
    time_left = serializers.SerializerMethodField()

    class Meta:
        model = EmailActivation
        fields = ['email', 'time_left']

    def get_time_left(self, obj):
        return obj.hours_to_expire_left()
