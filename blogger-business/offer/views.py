import json

from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    OfferSerializer, 
    OfferBusinessViewSerializer,
    OfferEditViewSerializer,
    OfferForApplicationViewSerializer,
)
from .services import (
    create_new_offer, 
    get_offers_for_blogger,
    get_offers_for_business,
    get_offer_by_id,
    get_offer_by_id_secured,
    edit_offer_by_id_secured,
    delete_offer_by_id_secured,
)
from account.decorators import allowed_users
from application.models import Application
from application.services import create_application, delete_application
from BloggerBusiness.utils import querydict_to_dict
from offer.models import Offer


@allowed_users(["BLOGGER"])
def dashboard_view(request):
    return render(request, "offer/dashboard.html", {})


@allowed_users(["BUSINESS"])
def offers_view(request):
    return render(request, "offer/offers.html", {})


@allowed_users(["BUSINESS"])
def offers_create_view(request):
    return render(request, "offer/create-edit-offers.html", {})


@allowed_users(["BUSINESS"])
def offers_edit_view(request, offer_id: str):
    business = request.user.business
    try:
        offer = get_offer_by_id_secured(business=business, offer_id=offer_id)
    except Offer.DoesNotExist:
        raise Http404
    except PermissionError:
        raise PermissionDenied

    return render(request, "offer/create-edit-offers.html")


@api_view(["GET"])
@allowed_users(["BLOGGER"])
def fetch_dashboard_offers(request):
    blogger = request.user.blogger
    offers = get_offers_for_blogger(blogger=blogger)
    offers_serializer = OfferSerializer(offers, many=True)
    return Response(json.dumps(offers_serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def fetch_business_offers(request):
    business = request.user.business
    offers = get_offers_for_business(business=business)
    offers_serializer = OfferBusinessViewSerializer(offers, many=True)
    return Response(json.dumps(offers_serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def fetch_offers_for_applications(request):
    business = request.user.business
    offers = get_offers_for_business(business=business)
    offers_serializer = OfferForApplicationViewSerializer(offers, many=True)
    return Response(json.dumps(offers_serializer.data), status=200)


@api_view(["POST"])
@allowed_users(["BUSINESS"])
def create_offer(request):
    data = querydict_to_dict(request.POST)
    image = request.FILES.get("image")
    business = request.user.business
    create_new_offer(data=data, image=image, business=business)
    return Response({"message": "You have created new offer"}, 201)


@api_view(["POST"])
@allowed_users(["BUSINESS"])
def edit_offer(request, offer_id: str):
    data = querydict_to_dict(request.POST)
    image = request.FILES.get("image")
    business = request.user.business
    print(data)
    try:
        offer = edit_offer_by_id_secured(data=data, image=image, offer_id=offer_id, business=business)
    except Offer.DoesNotExist:
        return Response({"message": f"Offer with id-{offer_id} does not exist"}, status=404)
    except PermissionError:
        return Response({"message": "You are not allowed to edit this offer"}, status=403)

    return Response({"message": "You have edited your offer"}, status=200)


@api_view(["POST", "DELETE"])
@allowed_users(["BUSINESS"])
def delete_offer(request, offer_id:str):
    business = request.user.business
    try:
        delete_offer_by_id_secured(business=business, offer_id=offer_id)
    except Offer.DoesNotExist:
        return Response({"message": f"Offer with id-{offer_id} does not exist"}, status=404)
    except PermissionError:
        return Response({"message": "You are not allowed to delete this offer"}, status=403)
    return Response({"message": "You have deleted your offer"}, status=200)


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def get_offer_for_edit(request, offer_id: str):
    business = request.user.business
    try:
        offer = get_offer_by_id_secured(business=business, offer_id=offer_id)
    except Offer.DoesNotExist:
        return Response({"message": f"Offer with id-{offer_id} does not exist"}, status=404)
    except PermissionError:
        return Response({"message": "You are not allowed to edit this offer"}, status=403)
    
    offer_serializer = OfferEditViewSerializer(offer)
    return Response(json.dumps(offer_serializer.data), status=200)


@api_view(["POST"])
@allowed_users(["BLOGGER"])
def rate_offer(request):
    offer_id = request.data.get("offerId")
    upvote = request.data.get("upvote")
    try:
        offer = get_offer_by_id(offer_id=offer_id)
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
    offer_id = request.data.get("offerId")
    business = request.user.business
    try:
        offer = get_offer_by_id_secured(business=business, offer_id=offer_id)
    except Offer.DoesNotExist:
        return Response({"message": f"There is no offer with id {offer_id}"}, status=404)
    except PermissionError:
        return Response({"message": "You are not allowed to cancel rate of this offer"})
    
    try:
        deleted = delete_application(
            offer=offer,
            blogger=request.user.blogger
        )
    except Application.DoesNotExist:
        return Response({"message": f"There is no application from you to offer with id {offer_id}"}, status=404)

    return Response({"message": "Vote was cancelled"}, status=200)