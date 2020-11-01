from django.db import models

from blogger.models import Blogger
from business.models import Business
from offer.models import Offer


class Application(models.Model):
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    upvote = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)


class ApplicationRate(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    upvote = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    