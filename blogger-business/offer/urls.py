from django.urls import path

from . import views


app_name = "offer"


urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("offers/actions/", views.offers_actions_view, name="actions"),
    path("offers/create/", views.offers_create_view, name="create"),
    path("api/offers/create/", views.create_offer, name="create-complete"),
    path("api/offers/fetch/", views.fetch_dashboard_offers, name="fetch-offers"),
    path("api/offers/rate/", views.rate_offer, name="rate-offer"),
    path("api/offers/rate/cancel/", views.cancel_rate_offer, name="cancel-rate-offer"),
]
