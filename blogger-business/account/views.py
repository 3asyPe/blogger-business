import json

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from .services import (
    send_password_email,
    custom_login,
    get_next_url_after_login,
    get_next_path,
    username_exists,
    email_exists,
)
from account.decorators import unauthenticated_user, allowed_users
from blogger.models import Blogger
from blogger.serializers import (
    BloggerSerializer,
    ImageInfoBloggerSerializer,
)
from blogger.services import (
    register_blogger,
    edit_blogger_profile_image,
)
from BloggerBusiness.utils import querydict_to_dict

from business.serializers import (
    BusinessSerializer,
    ImageInfoBusinessSerializer,
)
from business.services import (
    register_business,
    edit_business_profile_image,
)

from youtube.services import create_youtube_model

from rest_framework.decorators import api_view
from rest_framework.response import Response


User = settings.AUTH_USER_MODEL


@unauthenticated_user
def login_view(request):
    return render(request, "account/login.html", {})


@api_view(["POST"])
def login_account(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    try:
        user = custom_login(request=request, username=username, password=password) 
    except PermissionError:
        return Response({"message": "Your account isn't activated. Please check an email"}, status=403)
    if user is not None:
        next_url = get_next_url_after_login(user)
        data = {
            "message": "You was logged in successfuly",
            "next_url": next_url,
        }
        return Response(data, status=200)
    else:
        data = {
            "message": "You wasn't logged in",
        }
        return Response(data, status=401) 


def registration_view(request):
    account_type = request.GET.get("type") or request.POST.get("type")
    if account_type == "bl":
        return render(request, "blogger/registration.html", {})
    elif account_type == "bu":
        return render(request, "business/registration.html", {})
    else:
        return render(request, "account/registration-choice.html", {})


@api_view(["POST"])
def register_account(request):
    account_type = request.POST.get("accountType")
    print(request.POST)
    print(request.FILES)
    print(account_type)
    data = querydict_to_dict(request.POST)
    if account_type == "blogger":
        register_blogger(data=data, image=request.FILES.get("image"))
        return Response({"message": "Blogger account was created successfully"}, status=201)
    elif account_type == "business":
        register_business(data=data, image=request.FILES.get("image"))
        return Response({"message": "Business account was created successfully"}, status=201)
    else:
        return Response({"message": "Specify type of account you want to register"}, status=404)


@allowed_users(["BLOGGER", "BUSINESS"])
def profile_view(request):
    user = request.user
    if user.is_blogger:
        return render(request, "blogger/profile.html", {})
    elif user.is_business:
        return render(request, "business/profile.html", {})
    raise Http404


@api_view(["GET"])
@allowed_users(["BLOGGER", "BUSINESS"])
def fetch_profile_data(request):
    user = request.user
    if user.is_blogger:
        serializer = BloggerSerializer(user.blogger)
    elif user.is_business:
        serializer = BusinessSerializer(user.business)
    else:
        return Response({"message": "Account neither blogger or business"}, status=500)

    return Response(json.dumps(serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BLOGGER", "BUSINESS"])
def fetch_profile_image_data(request):
    user = request.user
    if user.is_blogger:
        serializer = ImageInfoBloggerSerializer(user.blogger)
    elif user.is_business:
        serializer = ImageInfoBusinessSerializer(user.business)
    else:
        return Response({"message": "Account neither blogger or business"}, status=500)
    
    return Response(json.dumps(serializer.data), status=200)


@api_view(["POST"])
@allowed_users(["BLOGGER", "BUSINESS"])
def edit_profile_image_data(request):
    try:
        image = request.FILES.get("image")
    except KeyError:
        raise KeyError("Image field isn't in the request")

    user = request.user
    if user.is_blogger:
        edit_blogger_profile_image(blogger=user.blogger, image=image)
    elif user.is_business:
        edit_business_profile_image(business=user.business, image=image)
    else:
        return Response({"message": "Account neither blogger or business"}, status=500)
    
    return Response({"message": "Profile image was edited successfuly"}, status=200)


@api_view(["POST"])
def username_check(request):
    try:
        username = request.data["username"]
    except KeyError:
        return Response({"message": "Data object doesn't have a username field"}, status=400)

    exists = username_exists(username)

    return Response({"exists": exists}, status=200)


@api_view(["POST"])
def email_check(request):
    try:
        email = request.data["email"]
    except KeyError:
        return Response({"message": "Data object doesn't have a email field"}, status=400)

    exists = email_exists(email)

    return Response({"exists": exists}, status=200)
