from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url

from typing import Optional


User = settings.AUTH_USER_MODEL


def create_user(username: str, password: str) -> Optional[User]:
    user = User.objects.create_user(username=username, password=password)
    return user


def send_password_email(email):
    pass


def custom_login(request, username: str, password: str) -> Optional[User]:
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        return user
    return None


def get_next_url_after_login(user: User) -> str:
    if user.is_blogger:
        return "/dashboard/"
    elif user.is_business:
        return "/offers/actions/"
    raise ValueError("User neither blogger or business")


def get_next_path(request, base_url='/') -> str:
    next_ = None
    next_ = request.GET.get('next')
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if is_safe_url(redirect_path, request.get_host()):
        return redirect_path
    else:
        return base_url
