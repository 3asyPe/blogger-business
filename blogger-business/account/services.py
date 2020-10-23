from django.conf import settings


User = settings.AUTH_USER_MODEL


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    return user


def send_password_email(email):
    pass
