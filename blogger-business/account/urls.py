from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    registration_view,
    profile_view,
    register_account,
    get_blog_languages,
    get_blog_specializations,
    login_view,
    login_account,
)


app_name = "account"


urlpatterns = [
    path("login", login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/login/complete", login_account, name="complete-login"),
    path("registration/", registration_view, name="registration"),
    path("api/registration/complete", register_account, name="complete-registration"),
    path("api/blog-languages", get_blog_languages, name="get-blog-languages"),
    path("api/blog-specializations", get_blog_specializations, name="get-blog-specializations"),
    path("profile/<int:blogger_id>/", profile_view, name="profile"),
]
