import json

from django.conf import settings
from django.shortcuts import render

from .serializers import BloggerSerializer
from account.decorators import allowed_users

from rest_framework.decorators import api_view
from rest_framework.response import Response


BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS


@allowed_users(["BLOGGER"])
@api_view(["GET"])
def fetch_blogger_profile_data(request):
    blogger_serializer = BloggerSerializer(request.user.blogger)
    
    return Response(json.dumps(blogger_serializer.data), status=200)


@api_view(["GET"])
def get_blog_languages(request):
    languages = [{
        "prefix": language[0],
        "language": language[1],
    } for language in BLOG_LANGUAGES]
    return Response({"languages": languages}, status=200)


@api_view(["GET"])
def get_blog_specializations(request):
    specializations = [{
        "prefix": specialization[0],
        "specialization": specialization[1],
    } for specialization in BLOG_SPECIALIZATIONS]
    return Response({"specializations": specializations}, status=200)