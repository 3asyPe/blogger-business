from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import QueryDict

from .models import Business

from account.models import Location
from account.services import create_user
from account.utils import generate_password
from emails.services import (
    send_verification_for_new_email,
    verification_email_is_sent,
)


User = get_user_model()


def edit_business_profile_contact(business: Business, data: dict) -> Business:
    try:
        business.site = data["site"]
    except KeyError:
        raise KeyError("Data object doesn't have site field")

    try:
        business.facebook = data["facebook"]
    except KeyError:
        raise KeyError("Data object doesn't have facebook field")

    try:
        business.instagram = data["instagram"]
    except KeyError:
        raise KeyError("Data object doesn't have instagram field")

    try:
        business.phone = data["phone"]
    except KeyError:
        raise KeyError("Data object doesn't have phone field")
    
    try:
        email = data["email"]
    except KeyError:
        raise KeyError("Data object doesn't have email field")
    user = business.user
    if user.email != email and not verification_email_is_sent(user=user, email=email):
        send_verification_for_new_email(user=user, email=email)

    business.save()
    return business


def edit_business_profile_info(business: Business, data: dict) -> Business:
    try:
        business.business_name = data["business_name"]
    except KeyError:
        raise KeyError("Data object doesn't have business_name field")

    try:
        business.business_owner_name = data["business_owner_name"]
    except KeyError:
        raise KeyError("Data object doesn't have business_owner_name field")

    location = _change_location(business=business, data=data)

    business.save()
    return business


def edit_business_profile_image(business: Business, image) -> Business:
    business.image = image
    business.save()
    return business


@transaction.atomic
def register_business(data: dict, image):
    user = _create_user_business(data=data)
    business = _create_business(data=data, image=image, user=user)
    return business


def _change_location(business: Business, data: dict) -> Location:
    location = business.location
    try:
        location.country = data["country"]
    except KeyError:
        raise KeyError("Data object doesn't have country field")

    try:
        location.city = data["city"]
    except KeyError:
        raise KeyError("Data object doesn't have city field")

    location.save()
    return location

    
def _create_business(data: dict, image, user: User) -> Business:
    location = _create_location(data=data)

    try:
        business = Business(
            user=user,
            image=image,
            business_name=data['business_name'],
            business_owner_name=data['business_owner_name'],
            email=data['email'],
            phone=data['phone'],
            location=location,
            site=data['site'],
            instagram=data['instagram'],
            facebook=data['facebook'],
        )
    except KeyError:
        raise KeyError("Data object doesn't have one of field that business account require")
    business.save()
    print(f"business-{business}")

    return business


def _create_location(data: dict) -> Location:
    try:
        location = Location.objects.create(country=data['country'], city=data['city'])
    except KeyError:
        raise KeyError("Data object doesn't have country or city field")
    print(f"location-{location}")
    location.save()

    return location


def _create_user_business(data: dict) -> User:
    password = generate_password()
    try:
        user = create_user(username=data['business_name'], email=data['email'], password=password)
    except KeyError:
        raise KeyError("Data object doesn't have field username or email field")
    print(f"user-{user}")

    return user
