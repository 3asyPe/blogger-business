from django.urls import path

from . import views


app_name = "blogger"


urlpatterns = [
    path("api/blog-languages", views.get_blog_languages, name="get-blog-languages"),
    path("api/blog-specializations", views.get_blog_specializations, name="get-blog-specializations"),
    path("api/blogger-profile-data/personal/", views.fetch_personal_info_blogger_profile_data, name="fetch-personal-info-blogger-profile-data"),
    path("api/blogger-profile-data/personal/edit/", views.edit_blogger_profile_personal_data, name="edit-blogger-profile-personal-data"),
    path("api/blogger-profile-data/blog/", views.fetch_blog_info_blogger_profile_data, name="fetch-blog-info-blogger-profile-data"),
    path("api/blogger-profile-data/blog/edit/", views.edit_blogger_profile_blog_data, name="edit-blogger-profile-blog-data"),
]
