import json

from django.core import serializers
from django.shortcuts import render
from django.forms.models import model_to_dict

from .services import get_applications_for_business
from .serializers import ApplicationSerializer
from account.decorators import allowed_users

from rest_framework.response import Response
from rest_framework.decorators import api_view


@allowed_users(["BUSINESS"])
def applications_view(request):
    return render(request, "application/applications.html", {})


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def fetch_applications(request):
    applications = get_applications_for_business(business=request.user.business)
    application_serializer = ApplicationSerializer(applications, many=True)
    return Response(json.dumps(application_serializer.data), status=200)
