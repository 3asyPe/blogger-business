from django.conf import settings
from django.db import models

from .utils import upload_image_path_blogger
from account.models import Location
from phonenumber_field.modelfields import PhoneNumberField


User = settings.AUTH_USER_MODEL
BLOG_LANGUAGES = settings.BLOG_LANGUAGES
BLOG_SPECIALIZATIONS = settings.BLOG_SPECIALIZATIONS
SEXES = settings.SEXES


class Blogger(models.Model):
    '''
        - User
        - Image *
        - Name *
        - Accounts in social media (instagram, youtube) *not during registraion
        - Email *
        - Phone *
        - Languages of blog (dropdown) (multiple choice)
        + Location *not via registraion
        - Blog specializations (0 < x < 3) *not during registraion
        - Sex *
        - Birthday *
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path_blogger, null=True, blank=True) 
    blog_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    youtube = models.CharField(max_length=255, null=True, blank=True)
    phone = PhoneNumberField()
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEXES)
    birthday = models.DateField()

    def __str__(self):
        return self.blog_name

    @property
    def is_active(self):
        return self.user.is_active
    

class BlogLanguage(models.Model):
    language = models.CharField(max_length=2, choices=BLOG_LANGUAGES)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE, related_name='languages')


class BlogSpecialization(models.Model):
    specialization = models.CharField(max_length=100, choices=BLOG_SPECIALIZATIONS)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE, related_name='specializations')

