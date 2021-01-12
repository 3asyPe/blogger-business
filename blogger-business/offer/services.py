import datetime

from django.db.models import QuerySet

from .models import (
    BloggerModel,
    BloggerModelLanguage,
    BloggerModelSpecialization,
    BloggerModelAgeGroup,
    ReceivingModel,
    Offer,
)
from account.models import Location
from account.utils import create_date_object
from blogger.models import Blogger, BlogLanguage, BlogSpecialization
from business.models import Business


def get_offers_for_blogger(blogger: Blogger):
    languages = BlogLanguage.objects.filter(blogger=blogger).values("language")
    blogger_model_languages_coincedences = BloggerModelLanguage.objects.filter(language__in=languages).values("blogger_model")
    specializations = BlogSpecialization.objects.filter(blogger=blogger).values("specialization")
    blogger_models = BloggerModelSpecialization.objects.filter(
        blogger_model__in=blogger_model_languages_coincedences,
        specialization__in=specializations,
    ).values("blogger_model")
    offers = Offer.objects.filter(blogger_model__in=blogger_models)

    return offers


def get_offers_for_business(business: Business) -> QuerySet[Offer]:
    offers = Offer.objects.filter(business=business)
    return offers


def get_offer_by_id_secured(business: Business, offer_id: str) -> Offer:
    offer = Offer.objects.get(offer_id=offer_id)
    if offer.business != business:
        raise PermissionError
    return offer


def delete_offer_by_id_secured(business: Business, offer_id: str):
    offer = Offer.objects.get(offer_id=offer_id)
    if offer.business != business:
        raise PermissionError
    offer.delete()


def edit_offer_by_id_secured(data: dict, image, offer_id: str, business: Business) -> Offer:
    offer = get_offer_by_id_secured(business=business, offer_id=offer_id)
    
    blogger_model =_change_blogger_model(data=data, offer=offer)
    receiving_model = _change_receiving_model(data=data, offer=offer)
    offer = _change_offer_data(data=data, image=image, offer=offer)

    return offer


def create_new_offer(data: dict, image, business: Business) -> Offer:
    receiving_model = _create_receiving_model(data=data)
    offer = _create_new_offer(
        data=data, 
        image=image, 
        business=business, 
        receiving_model=receiving_model,
    )
    blogger_model = _create_blogger_model(data=data, offer=offer)
    return offer
    

def get_offer_by_id(offer_id: str) -> Offer:
    offer = Offer.objects.get(offer_id=offer_id)
    return offer


def _change_offer_data(data: dict, image, offer: Offer) -> Offer:
    try:
        offer.title = data["title"]
    except KeyError:
        raise KeyError("Data object doesn't have title field")

    try:
        offer.description = data["description"]
    except KeyError:
        raise KeyError("Data object doesn't have description field")
    
    try:
        offer.conditions = data["conditions"]
    except KeyError:
        raise KeyError("Data object doesn't have conditions field")

    offer.price = data.get("price")

    if image:
        offer.image = image

    validity = _create_validity_object(data=data)
    offer.validity = validity

    offer.save()
    return offer


def _change_blogger_model(data: dict, offer: Offer) -> BloggerModel:
    blogger_model = offer.blogger_model
    try:
        blogger_model.min_subscribers = int(data["min_subscribers"])
    except KeyError:
        raise KeyError("Data object doesn't have min_subscribers field")
    
    try:
        blogger_model.max_subscribers = int(data["max_subscribers"])
    except KeyError:
        raise KeyError("Data object doesn't have max_subscribers field")

    try:
        blogger_model.sex = data["sex"]
    except KeyError:
        raise KeyError("Data object doesn't have sex field")

    _change_list_of_languages(data=data, blogger_model=blogger_model)
    _change_list_of_specializations(data=data, blogger_model=blogger_model)
    _change_list_of_age_groups(data=data, blogger_model=blogger_model)

    blogger_model.save()
    return blogger_model


def _change_receiving_model(data: dict, offer: Offer) -> ReceivingModel:
    receiving_model = offer.receiving_model
    try:
        if data["delivery"] == "true":
            receiving_model.delivery = True
        else:
            receiving_model.delivery = False
    except KeyError:
        raise KeyError("Data object doesn't have delivery field")

    receiving_model.address = data.get("address")

    receiving_model.save()
    return receiving_model


def _create_new_offer(data: dict, image, business: Business,
                      receiving_model: ReceivingModel) -> Offer:
    try:
        validity = _create_validity_object(data=data)
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
        )
    except KeyError:
        raise KeyError("Data object doesn't have enough information for new offer")
    offer.save()
    print(f"offer-{offer}")
    
    return offer


def _create_receiving_model(data: dict) -> ReceivingModel:
    try:
        delivery = data.get("delivery", False) == "true"
        receiving_model = ReceivingModel.objects.create(
            delivery=delivery,
            address=data.get("address"),
        )
    except KeyError:
        raise KeyError("Data object doesn't have price field")
    receiving_model.save()

    return receiving_model


def _create_blogger_model(data: dict, offer: Offer) -> BloggerModel:
    try:
        blogger_model = BloggerModel.objects.create(
            offer=offer,
            location=None,
            sex=data["sex"],
            min_subscribers=data["min_subscribers"],
            max_subscribers=data["max_subscribers"],
        )
    except KeyError:
        raise KeyError("Data object doesn't have enough information for blogger model")
    blogger_model.save()

    _create_list_of_languages(data=data, blogger_model=blogger_model)
    _create_list_of_specializations(data=data, blogger_model=blogger_model)
    _create_list_of_age_groups(data=data, blogger_model=blogger_model)

    return blogger_model


def _change_list_of_languages(data: dict, blogger_model: BloggerModel):
    try:
        new_languages = data["languages"]
    except KeyError:
        raise KeyError("Data object doesn't have languages field")

    if type(new_languages) == str:
        new_languages = [new_languages]

    cur_languages = BloggerModelLanguage.objects.filter(blogger_model=blogger_model)

    for cur_language in cur_languages:
        try:
            index_in_new = new_languages.index(cur_language.language)
            new_languages.pop(index_in_new)
        except ValueError:
            cur_language.delete()

    for new_language in new_languages:
        BloggerModelLanguage.objects.create(
            language=new_language, 
            blogger_model=blogger_model
        )


def _change_list_of_specializations(data: dict, blogger_model: BloggerModel):
    try:
        new_specializations = data["specializations"]
    except KeyError:
        raise KeyError("Data object doesn't have specializations field")

    if type(new_specializations) == str:
        new_specializations = [new_specializations]

    cur_specializations = BloggerModelSpecialization.objects.filter(blogger_model=blogger_model)

    for cur_specialization in cur_specializations:
        try:
            index_in_new = new_specializations.index(cur_specialization.specialization)
            new_specializations.pop(index_in_new)
        except ValueError:
            cur_specialization.delete()

    for new_specialization in new_specializations:
        BloggerModelSpecialization.objects.create(
            specialization=new_specialization, 
            blogger_model=blogger_model
        )


def _change_list_of_age_groups(data: dict, blogger_model: BloggerModel):
    try:
        new_age_groups = data["age_groups"]
    except KeyError:
        raise KeyError("Data object doesn't have age_groups field")

    if type(new_age_groups) == str:
        new_age_groups = [new_age_groups]

    cur_age_groups = BloggerModelAgeGroup.objects.filter(blogger_model=blogger_model)

    for cur_age_group in cur_age_groups:
        try:
            index_in_new = new_age_groups.index(cur_age_group.age_group)
            new_age_groups.pop(index_in_new)
        except ValueError:
            cur_age_group.delete()

    for new_age_group in new_age_groups:
        BloggerModelAgeGroup.objects.create(
            age_group=new_age_group, 
            blogger_model=blogger_model
        )


def _create_list_of_languages(data: dict, blogger_model: BloggerModel):
    try:
        languages = data.get("languages")
    except KeyError:
        raise KeyError("Data object doesn't have languages field")

    if type(languages) == str:
        languages = [languages]

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
    
    if type(specializations) == str:
        specializations = [specializations]

    for specialization in specializations:
        BloggerModelSpecialization.objects.create(
            specialization=specialization, 
            blogger_model=blogger_model
        )


def _create_list_of_age_groups(data: dict, blogger_model: BloggerModel):
    try:
        age_groups = data.get("age_groups")
    except KeyError:
        raise KeyError("Data object doesn't have age_groups field")
    
    if type(age_groups) == str:
        age_groups = [age_groups]

    for age_group in age_groups:
        BloggerModelAgeGroup.objects.create(
            age_group=age_group, 
            blogger_model=blogger_model
        )


def _create_validity_object(data:dict):
    try:
        day = data["day"]
    except KeyError:
        raise KeyError("Data object doesn't have day field")

    try:
        month = data["month"]
    except KeyError:
        raise KeyError("Data object doesn't have month field")

    try:
        year = data["year"]
    except KeyError:
        raise KeyError("Data object doesn't have year field")

    validity = create_date_object(day=day, month=month, year=year)

    return validity
