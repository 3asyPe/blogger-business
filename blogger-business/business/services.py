from django.contrib.auth import get_user_model
from django.http import QueryDict

from .models import Business

from account.models import Location
from account.utils import generate_password


User = get_user_model()


def register_business(data: dict, image):
    user = _create_user_business(data=data)
    business = _create_business(data=data, image=image, user=user)
    return business

    
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
        user = User.objects.create_user(username=data['business_name'], password=password)
    except KeyError:
        raise KeyError("Data object doesn't have field username")
    print(f"user-{user}")

    return user
