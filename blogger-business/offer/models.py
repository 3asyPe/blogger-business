from django.conf import settings
from django.db import models

from.utils import upload_image_path_offer

from account.models import Location
from business.models import Business


AGE_GROUPS = settings.AGE_GROUPS
SEXES = settings.SEXES + [("ANY", "ANY")]
BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS


class BloggerModel(models.Model):
    '''
        + Location
        + Languages of blog (dropdown) (several)
        + Specializations (0 < x < 5)
        - Age (dropdown of different age groups)
        - Number of subscribers (dropdown of ranges) (multiple choice)
        - Sex
    '''
    # if null -> any location is allowed
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    age_group = models.CharField(max_length=50)
    sex = models.CharField(max_length=3)


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
        - Timestamp *
        - Validity (calengar)
        + Blogger's model (sorting)
    '''
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path_offer, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    conditions = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    barter = models.BooleanField(default=True)
    receiving_model = models.OneToOneField(ReceivingModel, on_delete=models.SET_NULL, null=True, blank=True)
    validity = models.DateTimeField(null=True, blank=True)
    blogger_model = models.OneToOneField(BloggerModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BloggerModelLanguage(models.Model):
    language = models.CharField(max_length=2, choices=BLOG_LANGUAGES)
    blogger_model = models.ForeignKey(BloggerModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.language


class BloggerModelSpecialization(models.Model):
    specialization = models.CharField(max_length=100, choices=BLOG_SPECIALIZATIONS)
    blogger_model = models.ForeignKey(BloggerModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.specialization


class SubscribersNumberGroup(models.Model):
    group = models.IntegerField()
    blogger_model = models.ForeignKey(BloggerModel, on_delete=models.CASCADE)
