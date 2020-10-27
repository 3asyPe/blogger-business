from django.contrib.auth import get_user_model
from django.http import QueryDict

from .models import Business

from account.models import Location
from account.utils import generate_password


User = get_user_model()


def register_business(data: QueryDict, image):
    try:
        user = create_user_business(username=data['business_name'])
    except KeyError:
        raise KeyError("Data object doesn't have field username")
    print(f"user-{user}")

    try:
        location = Location.objects.create(country=data['country'], city=data['city'])
    except KeyError:
        raise KeyError("Data object doesn't have country or city field")
    print(f"location-{location}")

    location.save()

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
        raise KeyError("Data object doesn't have one of field that blogger account require")
    print(f"business-{business}")

    business.save()


def create_user_business(username):
    password = generate_password()
    user = User.objects.create_user(username=username, password=password)
    return user
