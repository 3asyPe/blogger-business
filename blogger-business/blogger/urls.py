from django.urls import path

from .views import profile_view


app_name = "blogger"


urlpatterns = [
    path("profile/<int:blogger_id>/", profile_view, name="profile"),
]
