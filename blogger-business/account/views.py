import json

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from .services import (
    send_password_email,
    custom_login,
    get_next_url_after_login,
    get_next_path,
)
from .forms import LoginForm
from account.decorators import unauthenticated_user, allowed_users
from blogger.models import Blogger
from blogger.services import register_blogger
from BloggerBusiness.utils import querydict_to_dict

from business.services import register_business

from rest_framework.decorators import api_view
from rest_framework.response import Response


User = settings.AUTH_USER_MODEL


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
    data = querydict_to_dict(request.POST)
    if account_type == "blogger":
        # send_password_email(email)
        register_blogger(data=data, image=request.FILES.get("image"))
        return Response({"message": "Blogger account was created successfully"}, status=201)
    elif account_type == "business":
        # send_password_email(email)
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

