from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import create_new_offer
from account.decorators import allowed_users
from BloggerBusiness.utils import querydict_to_dict


@allowed_users(["BLOGGER"])
def offers_view(request):
    return render(request, "offer/offers.html", {})


@allowed_users(["BUSINESS"])
def offers_actions_view(request):
    return render(request, "offer/actions.html", {})


@allowed_users(["BUSINESS"])
def offers_create_view(request):
    return render(request, "offer/create.html", {})


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
