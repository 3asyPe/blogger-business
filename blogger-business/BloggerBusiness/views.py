from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.response import Response


def home_view(request):
    return render(request, "pages/home.html", {})


def contact_view(request):
    return render(request, "base.html", {})


def about_view(request):
    return HttpResponse("<h1>About page</h1>")
