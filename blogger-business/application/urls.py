from django.urls import path

from . import views


app_name = "application"


urlpatterns = [
    path("applications/", views.applications_view, name="applications"),
]
