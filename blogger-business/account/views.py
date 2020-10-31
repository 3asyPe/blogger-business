import json

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from .services import (
    send_password_email,
    custom_login,
    get_next_url_after_login,
)
from .forms import LoginForm
from account.decorators import unauthenticated_user
from blogger.models import Blogger
from blogger.services import register_blogger
from BloggerBusiness.utils import querydict_to_dict

from business.services import register_business

from rest_framework.decorators import api_view
from rest_framework.response import Response


BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS


@unauthenticated_user
def login_view(request):
    return render(request, "account/login.html", {})


@api_view(["POST"])
def login_account(request):
    print(f"user-{request.user}")
    print(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = custom_login(request=request, username=username, password=password) 
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
    context = {}
    if account_type == "bl":
        return render(request, "blogger/registration.html", context)
    elif account_type == "bu":
        return render(request, "business/registration.html", context)
    else:
        raise ValueError("Specify type of account you want to register")


@api_view(["POST"])
def register_account(request):
    account_type = request.POST.get("accountType")
    print(request.POST)
    print(request.FILES)
    print(account_type)
    if account_type == "blogger":
        # send_password_email(email)
        data = querydict_to_dict(request.POST)
        register_blogger(data=data, image=request.FILES.get("image"))
        return Response({"message": "Blogger account was created successfully"}, status=201)
    elif account_type == "business":
        register_business(data=request.POST, image=request.FILES.get("image"))
        return Response({"message": "Business account was created successfully"}, status=201)
    else:
        return Response({"message": "Specify type of account you want to register"}, status=404)


def profile_view(request, blogger_id:int):
    try:
         blogger = Blogger.objects.get(id=blogger_id)
    except Blogger.DoesNotExist:
        return Http404(f"Blogger with id-{blogger_id} doesn't exist")
    context = {
        "blogger": blogger,
    }
    return render(request, "account/profile.html", context)


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
