from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.response import Response


def home_view(request):
    return JsonResponse({"message": "Home page"}, status=200)


def contact_view(request):
    return HttpResponse("<h1>Contact page</h1>")


def about_view(request):
    return HttpResponse("<h1>About page</h1>")
