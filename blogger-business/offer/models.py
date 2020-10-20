from django.conf import settings
from django.db import models

from account.models import Location
from blogger.models import Blogger
from business.models import Business


OFFER_STATES = settings.OFFER_STATES
AGE_GROUPS = settings.AGE_GROUPS
SEXES = settings.SEXES
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
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=True)
    age_group = models.CharField(max_length=120, choices=AGE_GROUPS)
    sex = models.CharField(max_length=1, choices=SEXES)


class BloggersRate(models.Model):
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    upvote = models.BooleanField()


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
        + Bloggers' rates (like, dislike)
        - State (requested, accepted, declined)
    '''
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    conditions = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    barter = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    validity = models.DateTimeField(null=True, blank=True)
    blogger_model = models.OneToOneField(BloggerModel, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, choices=OFFER_STATES)

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