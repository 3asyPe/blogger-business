from django.conf import settings
from django.db import models

from .utils import upload_image_path_business
from account.models import Location
from phonenumber_field.modelfields import PhoneNumberField


User = settings.AUTH_USER_MODEL


class Business(models.Model):
    '''
        - User
        - Image *
        - Name of business *
        - Name of owner *
        - Email *
        - Phone *
        + Location *not during registration
        - Site (link)
        - Instagram (link or name)
        - Facebook (link)
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path_business, null=True, blank=True) 
    business_name = models.CharField(max_length=120)
    business_owner_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = PhoneNumberField()
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=True)
    site = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.business_name

