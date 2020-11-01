import json

from django.core import serializers
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import create_new_offer, get_offers_for_blogger
from account.decorators import allowed_users
from application.models import Application
from application.services import create_application, delete_application
from BloggerBusiness.utils import querydict_to_dict
from offer.models import Offer


@allowed_users(["BLOGGER"])
def dashboard_view(request):
    return render(request, "offer/dashboard.html", {})


@allowed_users(["BUSINESS"])
def offers_actions_view(request):
    return render(request, "offer/actions.html", {})


@allowed_users(["BUSINESS"])
def offers_create_view(request):
    return render(request, "offer/create.html", {})


@api_view(["GET"])
@allowed_users(["BLOGGER"])
def fetch_dashboard_offers(request):
    blogger = request.user.blogger
    offers = get_offers_for_blogger(blogger=blogger)
    offers_json = serializers.serialize("json", offers)
    return Response(offers_json, status=200)


@api_view(["POST"])
@allowed_users(["BUSINESS"])
def create_offer(request):
    print(request.POST)
    print(request.FILES)
    data = querydict_to_dict(request.POST)
    image = request.FILES.get("image")
    business = request.user.business
    create_new_offer(data=data, image=image, business=business)
    return Response({"message": "You have created new offer"}, 201)


@api_view(["POST"])
@allowed_users(["BLOGGER"])
def rate_offer(request):
    print(request.data)
    offer_id = request.data.get("offerId")
    upvote = request.data.get("upvote")
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        return Response({"message": f"There is no offer with id {offer_id}"}, status=404)
    create_application(
        offer=offer,
        upvote=upvote,
        blogger=request.user.blogger,
    )
    return Response({"message": "Vote was applied"}, status=200)


@api_view(["POST"])
@allowed_users(["BLOGGER"])
def cancel_rate_offer(request):
    print(request.data)
    offer_id = request.data.get("offerId")
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        return Response({"message": f"There is no offer with id {offer_id}"}, status=404)
    
    try:
        deleted = delete_application(
            offer=offer,
            blogger=request.user.blogger
        )
        print(f"deleted-{deleted}")
    except Application.DoesNotExist:
        return Response({"message": f"There is no application from you to offer with id {offer_id}"}, status=404)

    return Response({"message": "Vote was cancelled"}, status=200)