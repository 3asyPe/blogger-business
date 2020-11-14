from django.urls import path

from . import views


app_name = "blogger"


urlpatterns = [
    path("api/blog-languages", views.get_blog_languages, name="get-blog-languages"),
    path("api/blog-specializations", views.get_blog_specializations, name="get-blog-specializations"),
    path("api/blogger-profile-data/", views.fetch_blogger_profile_data, name="fetch-blogger-profile-data"),
]
