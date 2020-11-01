from .models import Application
from offer.models import Offer
from blogger.models import Blogger


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

