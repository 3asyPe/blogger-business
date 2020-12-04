from django.urls import path

from . import views


app_name = "application"


urlpatterns = [
    path("applications/", views.applications_view, name="applications"),
    path("api/applications/rate/<int:application_id>/", views.rate_application, name="rate-application"),
    path("api/applications/fetch/<int:offer_id>/", views.fetch_application_for_offer, name="fetch-applications"),
]
