from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url

from emails.services import send_password_email
from typing import Optional


User = get_user_model()


def create_user(username: str, email: str, password: str) -> Optional[User]:
    user = User.objects.create_user(username=username, email=email, password=password)
    send_password_email(user=user, email=email, password=password)
    return user


def custom_login(request, username: str, password: str) -> Optional[User]:
    username = username.lower()
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if not user.is_active:
            raise PermissionError("User is not activated")
        login(request=request, user=user)
        return user
    return None


def get_next_url_after_login(user: User) -> str:
    if user.is_blogger:
        return "/dashboard/"
    elif user.is_business:
        return "/offers/"
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


def username_exists(username: str) -> bool:
    username = username.lower()
    qs = User.objects.filter(username=username)
    if qs.exists():
        return True
    return False


def email_exists(email: str) -> bool:
    email = email.lower()
    qs = User.objects.filter(email=email)
    if qs.exists():
        return True
    return False
