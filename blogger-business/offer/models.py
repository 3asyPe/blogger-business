from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from.utils import (
    upload_image_path_offer,
    create_offer_id,
)

from account.models import Location
from business.models import Business


AGE_GROUPS = settings.AGE_GROUPS
SEXES = settings.SEXES + [("ANY", "ANY")]
BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS


class ReceivingModel(models.Model):
    delivery = models.BooleanField(default=True)
    address = models.CharField(max_length=255, null=True, blank=True)


class Offer(models.Model):
    '''
        Offer
        - Business owner *
        - Title *
        - Description *
        - Conditions
        - Price (or barter)
        - Barter (or price)
        + Receiving model
        - Timestamp *
        - Validity (calengar)
        + Blogger's model (sorting)
    '''
    offer_id = models.CharField(max_length=8, null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path_offer, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    conditions = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    barter = models.BooleanField(default=True)
    receiving_model = models.OneToOneField(ReceivingModel, on_delete=models.SET_NULL, null=True, blank=True)
    validity = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BloggerModel(models.Model):
    '''
        + Location
        + Languages of blog (dropdown) (several)
        + Specializations (0 < x < 5)
        - Age (dropdown of different age groups)
        - Number of subscribers (min, max)
        - Sex
    '''
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, null=True, blank=True, related_name="blogger_model")
    # if null -> any location is allowed
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    sex = models.CharField(max_length=3, choices=SEXES)
    min_subscribers = models.IntegerField(default=500000)
    max_subscribers = models.IntegerField(default=1000000)

    def __str__(self):
        return f"{self.offer}"


class BloggerModelAgeGroup(models.Model):
    age_group = models.CharField(max_length=50, choices=AGE_GROUPS)
    blogger_model = models.ForeignKey(BloggerModel, on_delete=models.CASCADE, related_name="age_groups")

    def __str__(self):
        return f"{self.blogger_model.offer} - {self.age_group}"


class BloggerModelLanguage(models.Model):
    language = models.CharField(max_length=2, choices=BLOG_LANGUAGES)
    blogger_model = models.ForeignKey(BloggerModel, on_delete=models.CASCADE, related_name="languages")

    def __str__(self):
        return f"{self.blogger_model.offer} - {self.language}"


class BloggerModelSpecialization(models.Model):
    specialization = models.CharField(max_length=100, choices=BLOG_SPECIALIZATIONS)
    blogger_model = models.ForeignKey(BloggerModel, on_delete=models.CASCADE, related_name="specializations")

    def __str__(self):
        return f"{self.blogger_model.offer} - {self.specialization}"


def pre_save_offer_receiver(sender, instance, *args, **kwargs):
    if not instance.offer_id:
        create_offer_id(instance=instance, Klass=type(instance))


pre_save.connect(pre_save_offer_receiver, sender=Offer)
