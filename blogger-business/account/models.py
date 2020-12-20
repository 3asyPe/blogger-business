from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)


COUNTRIES = settings.COUNTRIES
CITIES = settings.CITIES


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_active=False, is_staff=False, is_admin=False):
        if not username: 
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")
        if not email:
            raise ValueError("User must have an email")

        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user
    

    def create_staffuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    objects = UserManager()

    @property
    def is_blogger(self):
        try:
            return self.blogger is not None
        except AttributeError:
            print("is not a blogger")
            return False

    @property
    def is_business(self):
        try:
            return self.business is not None
        except AttributeError:
            print("is not a business")
            return False

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    

class Location(models.Model):
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
