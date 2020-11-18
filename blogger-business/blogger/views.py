import json

from django.conf import settings
from django.shortcuts import render

from .serializers import (
    BloggerSerializer,
    ImageInfoBloggerSerializer,
    PersonalInfoBloggerSerializer,
    BlogInfoBloggerSerializer,
)
from .services import (
    edit_blogger_profile_image,
    edit_blogger_profile_personal_info,
    edit_blogger_profile_blog_info,
)
from account.decorators import allowed_users
from BloggerBusiness.utils import querydict_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response


BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS


@api_view(["GET"])
@allowed_users(["BLOGGER"])
def fetch_full_blogger_profile_data(request):
    blogger_serializer = BloggerSerializer(request.user.blogger)
    return Response(json.dumps(blogger_serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BLOGGER"])
def fetch_image_info_blogger_profile_data(request):
    blogger_serializer = ImageInfoBloggerSerializer(request.user.blogger)
    return Response(json.dumps(blogger_serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BLOGGER"])
def fetch_personal_info_blogger_profile_data(request):
    blogger_serializer = PersonalInfoBloggerSerializer(request.user.blogger)
    return Response(json.dumps(blogger_serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BLOGGER"])
def fetch_blog_info_blogger_profile_data(request):
    blogger_serializer = BlogInfoBloggerSerializer(request.user.blogger)
    return Response(json.dumps(blogger_serializer.data), status=200)


@api_view(["POST"])
@allowed_users(["BLOGGER"])
def edit_blogger_profile_image_data(request):
    blogger = request.user.blogger
    try:
        image = request.FILES.get("image")
    except KeyError:
        raise KeyError("Image field isn't in the request")

    edit_blogger_profile_image(blogger=blogger, image=image)
    
    return Response({"message": "Profile image was edited successfuly"}, status=200)


@api_view(["POST"])
@allowed_users(["BLOGGER"])
def edit_blogger_profile_personal_data(request):
    blogger = request.user.blogger
    data = querydict_to_dict(request.POST)
    print(data)
    edit_blogger_profile_personal_info(blogger=blogger, data=data)
    return Response({"message": "Profile personal info has been edited successfuly"}, status=200)


@api_view(["POST"])
@allowed_users(["BLOGGER"])
def edit_blogger_profile_blog_data(request):
    blogger = request.user.blogger
    data = querydict_to_dict(request.POST)
    print(data)
    edit_blogger_profile_blog_info(blogger=blogger, data=data)
    return Response({"message": "Profile blog info has been edited successfuly"}, status=200)


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