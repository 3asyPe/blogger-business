from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.response import Response


def home_view(request):
    return render(request, "pages/home.html", {})


def contact_view(request):
    return render(request, "base.html", {})


def about_view(request):
    return HttpResponse("pages/about.html")


def terms_of_use_view(request):
    return render(request, "pages/terms-of-use.html", {})


def privacy_policy_view(request):
    return render(request, "pages/privacy-policy.html")
