import json

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from blogger.models import Blogger

from rest_framework.decorators import api_view
from rest_framework.response import Response


BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS

GOOGLE_API_KEY = settings.GOOGLE_API_KEY


def registration_view(request):
    account_type = request.GET.get("type") or request.POST.get("type")
    context = {}
    if account_type == "bl":
        context["languages"] = BLOG_LANGUAGES
        context["specializations"] = BLOG_SPECIALIZATIONS
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
        return Response({"message": "Account was created successfully"}, status=201)
    elif account_type == "business":
        return Response({"message": "Account was created successfully"}, status=201)
    else:
        return Response({"message": "Specify type of account you want to register"}, status=404)


def profile_view(request, blogger_id:int):
    try:
         blogger = Blogger.objects.get(id=blogger_id)
    except Blogger.DoesNotExist:
        return Http404(f"Blogger with id-{blogger_id} doesn't exist")
    context = {
        "blogger": blogger,
        "GOOGLE_API_KEY": GOOGLE_API_KEY,
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
