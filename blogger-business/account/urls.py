from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

from . import views


app_name = "account"


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/login/complete", views.login_account, name="complete-login"),

    path("registration/", views.registration_view, name="registration"),
    path("api/registration/complete", views.register_account, name="complete-registration"),

    path("profile/", views.profile_view, name="profile"),
    path("settings/", RedirectView.as_view(url="/profile"), name="settings"),

    path("api/profile-data/", views.fetch_profile_data, name="fetch-full-profile-data"),
    path("api/profile-data/image/", views.fetch_profile_image_data, name="fetch-profile-image-data"),
    path("api/profile-data/image/edit/", views.edit_profile_image_data, name="edit-profile-image-data"),
]
