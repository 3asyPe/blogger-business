from django.urls import path

from . import views


app_name = "youtube"


urlpatterns = [
    path("api/youtube/get/", views.get_youtube, name="get-youtube"),
    path("api/youtube/refresh/", views.refresh_youtube_channel_existing, name="refresh-youtube-existing"),
    path("api/youtube/statistics/update/", views.update_statistics, name="update-statistics"),
]
