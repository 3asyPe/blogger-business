import json

from django.core import serializers
from django.shortcuts import render
from django.http import Http404

from .models import Application
from .services import (
    count_applications,
    get_applications_for_business,
    get_applications_by_offer,
    rate_application_by_id,
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


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def get_applications_count(request):
    business = request.user.business
    count = count_applications(business=business)
    return Response({"applications_count": count}, status=200)


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


@api_view(["POST"])
@allowed_users(["BUSINESS"])
def rate_application(request, application_id: int):
    data = request.POST
    upvote = data.get("upvote")
    if upvote is None:
        return Response({"message": f"Data object doesn't have upvote field"})
    elif upvote == "true":
        upvote = True
    else:
        upvote = False

    business = request.user.business
    try:
        rate_application_by_id(application_id=application_id, business=business, upvote=upvote)
    except Application.DoesNotExist:
        return Response({"message": f"Application with id-{application_id} doesn't exist"})

    return Response({"message": "You have rated an application"}, status=200)
