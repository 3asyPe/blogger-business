from django.urls import path

from . import views


app_name = "youtube"


urlpatterns = [
    path("api/youtube/get/", views.get_youtube, name="get-youtube"),
]
