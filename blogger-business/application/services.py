from django.db.models.query import QuerySet

from .models import Application
from blogger.models import Blogger
from business.models import Business
from offer.models import Offer


def create_application(offer, upvote, blogger) -> Application:
    qs = Application.objects.filter(
        offer=offer,
        blogger=blogger
    )
    if qs.exists():
        application = qs.first()
        application.upvote = upvote
        application.save()
    else:
        application = Application.objects.create(
            offer=offer,
            blogger=blogger,
            upvote=upvote
        )
    return application


def delete_application(offer: Offer, blogger: Blogger) -> bool:
    try:
        application = Application.objects.get(
            offer=offer,
            blogger=blogger
        )
    except Application.DoesNotExist:
        raise Application.DoesNotExist

    deleted = application.delete()

    return deleted


def get_applications_by_offer(offer: Offer) -> QuerySet[Application]:
    applications = Application.objects.filter(offer=offer, upvote=True)
    return applications


def get_applications_for_business(business: Business) -> QuerySet[Application]:
    offers = Offer.objects.filter(business=business)
    applications = Application.objects.filter(offer__in=offers, upvote=True)
    return applications
