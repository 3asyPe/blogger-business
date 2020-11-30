from django.urls import path

from . import views


app_name = "offer"


urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("offers/<int:offer_id>/", views.offer_details_view, name="offer"),
    path("offers/", views.offers_view, name="offers"),
    path("offers/create/", views.offers_create_view, name="create"),
    path("offers/edit/<int:offer_id>", views.offers_edit_view, name="offer-edit"),
    path("api/offers/create/", views.create_offer, name="create-complete"),
    path("api/offers/<int:offer_id>/", views.get_offer, name="get-offer"),
    path("api/dashboard/fetch/", views.fetch_dashboard_offers, name="fetch-offers-blogger"),
    path("api/offers/fetch/", views.fetch_business_offers, name="fetch-offers-business"),
    path("api/offers/rate/", views.rate_offer, name="rate-offer"),
    path("api/offers/rate/cancel/", views.cancel_rate_offer, name="cancel-rate-offer"),
]
