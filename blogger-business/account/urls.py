from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

from .views import (
    registration_view,
    profile_view,
    register_account,
    login_view,
    login_account,
)


app_name = "account"


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/login/complete", login_account, name="complete-login"),

    path("registration/", registration_view, name="registration"),
    path("api/registration/complete", register_account, name="complete-registration"),

    path("profile/", profile_view, name="profile"),
    path("settings/", RedirectView.as_view(url="/profile"), name="settings"),
]
