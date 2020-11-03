from django.urls import path

from . import views


app_name = "application"


urlpatterns = [
    path("applications/", views.applications_view, name="applications"),
    path("applications/<int:application_id>/", views.application_details_view, name="application-details"),
    path("api/applications/fetch/", views.fetch_applications, name="fetch-applications"),
]
