from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import QueryDict

from .models import (
    Blogger,
    BlogLanguage, 
    BlogSpecialization
)

from account.models import Location
from account.utils import generate_password, create_birthday_object


User = get_user_model()


def register_blogger(data: QueryDict, image):
    try:
        user = create_user_blogger(username=data['blog_name'])
    except KeyError:
        raise KeyError("Data object doesn't have field username")
    print(f"user-{user}")

    try:
        birthday = create_birthday_object(
            day=data['day'],
            month=data['month'],
            year=data['year']
        )
    except KeyError:
        raise KeyError("Data object doesn't have day, month or year field")
    print(f"birthday-{birthday}")

    try:
        blogger = Blogger(
            user=user,
            image=image,
            blog_name=data['blog_name'],
            email=data['email'],
            phone=data['phone'],
            sex=data['sex'],
            birthday=birthday,
        )
    except KeyError:
        raise KeyError("Data object doesn't have one of field that blogger account require")
    print(f"blogger-{blogger}")

    blogger.save()

    try:
        location = Location.objects.create(country=data['country'], city=data['city'], blogger=blogger)
    except KeyError:
        raise KeyError("Data object doesn't have country or city field")
    print(f"location-{location}")

    try:
        languages = create_list_of_languages(languages=data['languages'], blogger=blogger)
    except KeyError:
        raise KeyError("Data object doesn't have field with languages")
    print(f"languages-{languages}")

    try:
        specializations = create_list_of_specializations(specializations=data['specializations'], blogger=blogger)
    except KeyError:
        raise KeyError("Data object doesn't have field with specializations")
    print(f"specializations-{specializations}")
    

def create_user_blogger(username):
    password = generate_password()
    user = User.objects.create_user(username=username, password=password)
    return user


def create_list_of_languages(languages, blogger:Blogger):
    for language in languages:
        language = BlogLanguage(language=language, blogger=blogger)
        language.save()


def create_list_of_specializations(specializations, blogger:Blogger):
    for specialization in specializations:
        specialization = BlogSpecialization(specialization=specialization, blogger=blogger)
        specialization.save()
