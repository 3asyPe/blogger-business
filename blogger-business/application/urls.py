from django.urls import path

from . import views


app_name = "application"


urlpatterns = [
    path("applications/", views.applications_view, name="applications"),
    path("api/applications/count/", views.get_applications_count, name="applications-count"),
    path("api/applications/rate/<int:application_id>/", views.rate_application, name="rate-application"),
    path("api/applications/fetch/<str:offer_id>/", views.fetch_application_for_offer, name="fetch-applications"),
]
