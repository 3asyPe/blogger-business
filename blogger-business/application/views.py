import json

from django.core import serializers
from django.shortcuts import render
from django.http import Http404

from .models import Application
from .services import (
    get_applications_for_business,
    get_applications_by_offer,
)
from .serializers import ApplicationSerializer
from account.decorators import allowed_users
from offer.models import Offer
from offer.services import get_offer_by_id

from rest_framework.response import Response
from rest_framework.decorators import api_view


@allowed_users(["BUSINESS"])
def applications_view(request):
    return render(request, "application/applications.html", {})


@allowed_users(["BUSINESS"])
def application_details_view(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        raise Http404(f"Application with id {application_id} doesn't exist")
    context = {
        "application" : application
    }
    return render(request, "application/details.html", context)


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def fetch_applications(request):
    applications = get_applications_for_business(business=request.user.business)
    application_serializer = ApplicationSerializer(applications, many=True)
    return Response(json.dumps(application_serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def fetch_application_for_offer(request, offer_id:int):
    try:
        offer = get_offer_by_id(offer_id=offer_id)
    except Offer.DoesNotExist:
        return Response({"message": f"Offer with id-{offer_id} doesn't exist"})

    applications = get_applications_by_offer(offer=offer)
    applications_serializer = ApplicationSerializer(applications, many=True)
    return Response(json.dumps(applications_serializer.data), status=200)
