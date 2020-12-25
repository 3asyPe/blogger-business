from django.db.models.query import QuerySet

from .models import (
    Application,
    ApplicationRate,
)
from blogger.models import Blogger
from business.models import Business
from offer.models import Offer


def count_applications(business):
    offers = Offer.objects.filter(business=business)
    count = Application.objects.filter(offer__in=offers, upvote=True, application_rate=None).count()
    return count


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


def rate_application_by_id(application_id: int, business: Business, upvote: bool):
    application = Application.objects.get(id=application_id)
    application_rate = ApplicationRate.objects.create(
        application=application,
        business=business,
        upvote=upvote,
    )


def get_applications_by_offer(offer: Offer) -> QuerySet[Application]:
    applications = Application.objects.filter(offer=offer, upvote=True, application_rate=None)
    return applications


def get_applications_for_business(business: Business) -> QuerySet[Application]:
    offers = Offer.objects.filter(business=business)
    print(offers)
    applications = Application.objects.filter(offer__in=offers, upvote=True)
    return applications
