import datetime

from django.db.models import QuerySet

from .models import (
    BloggerModel,
    BloggerModelLanguage,
    BloggerModelSpecialization,
    SubscribersNumberGroup,
    ReceivingModel,
    Offer,
)
from account.models import Location
from blogger.models import Blogger, BlogLanguage, BlogSpecialization
from business.models import Business


def get_offers_for_blogger(blogger: Blogger):
    languages = BlogLanguage.objects.filter(blogger=blogger).values("language")
    print(f"languages-{languages}")
    blogger_model_languages_coincedences = BloggerModelLanguage.objects.filter(language__in=languages).values("blogger_model")
    print(f"blogger_model_languages_coincedences-{blogger_model_languages_coincedences}")
    specializations = BlogSpecialization.objects.filter(blogger=blogger).values("specialization")
    print(f"specializations-{specializations}")
    blogger_models = BloggerModelSpecialization.objects.filter(
        blogger_model__in=blogger_model_languages_coincedences,
        specialization__in=specializations,
    ).values("blogger_model")
    offers = Offer.objects.filter(blogger_model__in=blogger_models)

    return offers


def get_offers_for_business(business: Business) -> QuerySet[Offer]:
    offers = Offer.objects.filter(business=business)
    return offers


def create_new_offer(data:dict, image, business:Business) -> Offer:
    blogger_model = _create_blogger_model(data=data)
    receiving_model = _create_receiving_model(data=data)
    offer = _create_new_offer(
        data=data, 
        image=image, 
        business=business, 
        receiving_model=receiving_model,
        blogger_model=blogger_model,    
    )
    return offer
    

def _create_new_offer(data: dict, image, business: Business,
                      receiving_model: ReceivingModel, blogger_model: BloggerModel) -> Offer:
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
        raise KeyError("Data object doesn't have enough information for new offer")
    offer.save()
    print(f"offer-{offer}")
    
    return offer


def _create_receiving_model(data: dict) -> ReceivingModel:
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

    return receiving_model

def _create_blogger_model(data: dict) -> BloggerModel:
    try:
        blogger_model = BloggerModel.objects.create(
            location=None,
            age_group=data.get("age_group"),
            sex=data.get("sex"),
        )
    except KeyError:
        raise KeyError("Data object doesn't have enough information for blogger model")
    blogger_model.save()
    print(f"blogger_model-{blogger_model}")

    _create_list_of_languages(data=data, blogger_model=blogger_model)
    _create_list_of_specializations(data=data, blogger_model=blogger_model)
    _create_list_of_subscribers_number_groups(data=data, blogger_model=blogger_model)

    return blogger_model


def _create_list_of_subscribers_number_groups(data: dict, blogger_model: BloggerModel):
    try:
        subscribers_number_groups = data.get("subscribers_number_groups")
    except KeyError:
        raise KeyError("Data object doesn't have subscribers_number_groups field")
    for group in subscribers_number_groups:
        SubscribersNumberGroup.objects.create(
            group=group,
            blogger_model=blogger_model
        )


def _create_list_of_languages(data: dict, blogger_model: BloggerModel):
    try:
        languages = data.get("languages")
    except KeyError:
        raise KeyError("Data object doesn't have languages field")
    for language in languages:
        BloggerModelLanguage.objects.create(
            language=language, 
            blogger_model=blogger_model
        )



def _create_list_of_specializations(data: dict, blogger_model: BloggerModel):
    try:
        specializations = data.get("specializations")
    except KeyError:
        raise KeyError("Data object doesn't have specializations field")
    for specialization in specializations:
        BloggerModelSpecialization.objects.create(
            specialization=specialization, 
            blogger_model=blogger_model
        )
