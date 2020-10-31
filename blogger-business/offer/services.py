import datetime

from .models import (
    BloggerModel,
    BloggerModelLanguage,
    BloggerModelSpecialization,
    ReceivingModel,
    Offer,
)
from account.models import Location
from business.models import Business


def create_new_offer(data:dict, image, business:Business):
    try:
        blogger_model = BloggerModel.objects.create(
            location=None,
            age_group=data.get("age_group"),
            subscribers_number_group=data.get("subscribers_number_group"),
            sex=data.get("sex"),
        )
    except KeyError:
        raise KeyError("Data object doesn't have enough information for blogger model")
    blogger_model.save()
    print(f"blogger_model-{blogger_model}")

    try:
        languages = create_list_of_languages(
            languages=data.get("languages"),
            blogger_model=blogger_model,
        )
    except KeyError:
        raise KeyError("Data object doesn't have languages field")
    print(f"languages-{languages}")

    try:
        specializations = create_list_of_specializations(
            specializations=data.get("specializations"),
            blogger_model=blogger_model,
        )
    except KeyError:
        raise KeyError("Data object doesn't have specializations field")
    print(f"specializations-{specializations}")

    try:
        delivery = data.get("delivery", False) == "on"
        receiving_model = ReceivingModel.objects.create(
            delivery=delivery,
            address=data.get("address"),
        )
    except KeyError:
        raise KeyError("Data object doesn't have price field")
    receiving_model.save()
    print(f"receiving_model-{receiving_model}")

    try:
        validity = datetime.datetime.strptime(data.get("validity"), "%Y-%m-%d")
        barter = data.get("barter", False) == "on"
        price = int(data.get("price")) if data.get("price") else None
        offer = Offer.objects.create(
            business=business,
            image=image,
            title=data.get("title"),
            description=data.get("description"),
            conditions=data.get("conditions"),
            price=price,
            barter=barter,
            receiving_model=receiving_model,
            validity=validity,
            blogger_model=blogger_model,
        )
    except KeyError:
        raise KeyError("Data obj")
    offer.save()
    print(f"offer-{offer}")


def create_list_of_languages(languages, blogger_model:BloggerModel):
    for language in languages:
        language = BloggerModelLanguage(language=language, blogger_model=blogger_model)
        language.save()


def create_list_of_specializations(specializations, blogger_model:BloggerModel):
    for specialization in specializations:
        specialization = BloggerModelSpecialization(specialization=specialization, blogger_model=blogger_model)
        specialization.save()
