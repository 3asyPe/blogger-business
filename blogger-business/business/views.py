import json

from django.shortcuts import render

from .serializers import (
    BusinessInfoSerializer,
    BusinessContactSerializer,
)
from .services import (
    edit_business_profile_info,
    edit_business_profile_contact,
)
from account.decorators import allowed_users
from BloggerBusiness.utils import querydict_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def fetch_business_info_profile_data(request):
    business_serializer = BusinessInfoSerializer(request.user.business)
    return Response(json.dumps(business_serializer.data), status=200)


@api_view(["GET"])
@allowed_users(["BUSINESS"])
def fetch_business_contact_profile_data(request):
    business_serializer = BusinessContactSerializer(request.user.business)
    return Response(json.dumps(business_serializer.data), status=200)


@api_view(["POST"])
@allowed_users(["BUSINESS"])
def edit_business_info_profile_data(request):
    business = request.user.business
    data = querydict_to_dict(request.POST)
    print(data)
    edit_business_profile_info(business=business, data=data)
    return Response({"message": "Profile business info has been edited successfuly"}, status=200)


@api_view(["POST"])
@allowed_users(["BUSINESS"])
def edit_business_contact_profile_data(request):
    business = request.user.business
    data = querydict_to_dict(request.POST)
    print(data)
    edit_business_profile_contact(business=business, data=data)
    return Response({"message": "Profile business contact has been edited successfuly"}, status=200)
