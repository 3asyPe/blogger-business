from django.contrib.auth import get_user_model

from .models import (
    Blogger,
    BlogLanguage, 
    BlogSpecialization
)

from account.models import Location
from account.services import create_user
from account.utils import generate_password, create_date_object
from emails.services import send_verification_for_new_email


User = get_user_model()


def edit_blogger_profile_image(blogger: Blogger, image) -> Blogger:
    blogger.image = image
    blogger.save()
    return blogger


def edit_blogger_profile_personal_info(blogger: Blogger, data: dict) -> Blogger:
    try:
        blogger.blog_name = data["blog_name"]
    except KeyError:
        raise KeyError("Data object doesn't have blog_name")
    
    location = _change_location(blogger=blogger, data=data)
    
    birthday = _create_birthday_object(data=data)
    blogger.birthday = birthday
    
    blogger.save()
    return blogger


def edit_blogger_profile_blog_info(blogger: Blogger, data: dict) -> Blogger:
    _change_list_of_languages(data=data, blogger=blogger)
    _change_list_of_specializations(data=data, blogger=blogger)
    
    try:
        blogger.phone = data["phone"]
    except KeyError:
        raise KeyError("Data object doesn't have phone field")

    try:
        email = data["email"]
    except KeyError:
        raise KeyError("Data object doesn't have email field")
    user = blogger.user
    if user.email != email:
        send_verification_for_new_email(user=user, email=email)

    blogger.save()
    return blogger


def register_blogger(data: dict, image) -> Blogger:
    user = _create_user_blogger(data=data)
    blogger = _create_blogger(data=data, image=image, user=user)
    return blogger
    

def _create_blogger(data: dict, image, user: User) -> Blogger:
    birthday = _create_birthday_object(data=data)
    location = _create_location(data=data)
    
    try:
        blogger = Blogger(
            user=user,
            image=image,
            blog_name=data['blog_name'],
            email=data['email'],
            phone=data['phone'],
            location=location,
            sex=data['sex'],
            birthday=birthday,
        )
    except KeyError:
        raise KeyError("Data object doesn't have one of field that blogger account require")
    blogger.save()
    print(f"blogger-{blogger}")

    _create_list_of_languages(data=data, blogger=blogger)
    _create_list_of_specializations(data=data, blogger=blogger)
    
    return blogger


def _change_location(blogger: Blogger, data: dict) -> Location:
    location = blogger.location
    try:
        location.country = data["country"]
    except KeyError:
        raise KeyError("Data object doesn't have country field")

    try:
        location.city = data["city"]
    except KeyError:
        raise KeyError("Data object doesn't have city field")

    location.save()
    return location


def _create_location(data: dict) -> Location:
    try:
        location = Location.objects.create(country=data['country'], city=data['city'])
    except KeyError:
        raise KeyError("Data object doesn't have country or city field")
    print(f"location-{location}")
    location.save()

    return location


def _create_birthday_object(data: dict):
    try:
        birthday = create_date_object(
            day=data['day'],
            month=data['month'],
            year=data['year']
        )
    except KeyError:
        raise KeyError("Data object doesn't have day, month or year field")
    print(f"birthday-{birthday}")

    return birthday


def _create_user_blogger(data: dict) -> User:
    password = generate_password()
    try:
        user = create_user(username=data['blog_name'], email=data['email'], password=password)
    except KeyError:
        raise KeyError("Data object doesn't have username or email field")
    print(f"user-{user}")
    return user


def _change_list_of_languages(data: dict, blogger: Blogger):
    try:
        new_languages = data["languages"]
    except KeyError:
        raise KeyError("Data object doesn't have languages field")

    if type(new_languages) == str:
        new_languages = [new_languages]

    cur_languages = BlogLanguage.objects.filter(blogger=blogger)

    for cur_language in cur_languages:
        try:
            index_in_new = new_languages.index(cur_language.language)
            new_languages.pop(index_in_new)
        except ValueError:
            cur_language.delete()

    for new_language in new_languages:
        BlogLanguage.objects.create(
            language=new_language, 
            blogger=blogger
        )


def _change_list_of_specializations(data: dict, blogger: Blogger):
    try:
        new_specializations = (data["specializations"])
    except KeyError:
        raise KeyError("Data object doesn't have specializations field")

    if type(new_specializations) == str:
        new_specializations = [new_specializations]

    cur_specializations = BlogSpecialization.objects.filter(blogger=blogger)

    for cur_specialization in cur_specializations:
        try:
            index_in_new = new_specializations.index(cur_specialization.specialization)
            new_specializations.pop(index_in_new)
        except ValueError:
            cur_specialization.delete()

    for new_specialization in new_specializations:
        BlogSpecialization.objects.create(
            specialization=new_specialization, 
            blogger=blogger
        )


def _create_list_of_languages(data: dict, blogger: Blogger):
    try:
        languages = data.get("languages")
    except KeyError:
        raise KeyError("Data object doesn't have languages field")

    if type(languages) == str:
        languages = [languages]

    for language in languages:
        BlogLanguage.objects.create(
            language=language, 
            blogger=blogger
        )


def _create_list_of_specializations(data: dict, blogger: Blogger):
    try:
        specializations = data.get("specializations")
    except KeyError:
        raise KeyError("Data object doesn't have specializations field")

    if type(specializations) == str:
        specializations = [specializations]

    for specialization in specializations:
        BlogSpecialization.objects.create(
            specialization=specialization, 
            blogger=blogger
        )
