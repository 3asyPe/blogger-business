from BloggerBusiness.utils import (
    upload_image_path,
    generate_random_key,
)


def upload_image_path_offer(*args, **kwargs):
    return upload_image_path(*args, **kwargs, prefix="offer")


def create_offer_id(instance, Klass):
    offer_id = generate_random_key(length=8)
    qs = Klass.objects.filter(offer_id=offer_id)
    while qs.exists():
        offer_id = Klass.objects.filter(offer_id=offer_id)
        qs = Klass.objects.filter(offer_id=offer_id)
    instance.offer_id = offer_id
