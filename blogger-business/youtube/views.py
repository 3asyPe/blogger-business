import json

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Youtube
from .services import (
    get_youtube_by_blogger,
    update_channel_info,
)
from .serializers import (
    YoutubeSerializer,
    YoutubeStatisticsSerializer,
)
from account.decorators import allowed_users


@api_view(["GET"])
@allowed_users(["BLOGGER"])
def get_youtube(request):
    blogger = request.user.blogger
    try:
        youtube = get_youtube_by_blogger(blogger=blogger)
    except Youtube.DoesNotExist():
        return Response({"message": "youtube_does_not_exist"}, status=404)

    serializer = YoutubeSerializer(youtube)
    return Response(json.dumps(serializer.data), status=200)


@api_view(["POST"])
@allowed_users(["BLOGGER"])
def refresh_youtube_channel_existing(request):
    blogger = request.user.blogger
    try:
        youtube = get_youtube_by_blogger(blogger=blogger)
    except Youtube.DoesNotExist():
        return Response({"message": "youtube_does_not_exist"}, status=404)

    updated = update_channel_info(youtube)
    if updated:
        serializer = YoutubeSerializer(youtube)
        return Response(json.dumps(serializer.data), status=200)
    else:
        return Response({"message": "updating_channel_error"}, status=400)
