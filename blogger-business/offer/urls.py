from django.urls import path

from . import views


app_name = "offer"


urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("offers/", views.offers_view, name="offers"),
    path("offers/create/", views.offers_create_view, name="create"),
    path("offers/edit/<str:offer_id>", views.offers_edit_view, name="offer-edit"),
    path("api/offers/get/<str:offer_id>/", views.get_offer_for_edit, name="get-offer"),
    path("api/offers/create/", views.create_offer, name="create-complete"),
    path("api/offers/edit/<str:offer_id>/", views.edit_offer, name="edit-complete"),
    path("api/offers/delete/<str:offer_id>/", views.delete_offer, name="delete"),
    path("api/dashboard/fetch/", views.fetch_dashboard_offers, name="fetch-offers-blogger"),
    path("api/offers/fetch/", views.fetch_business_offers, name="fetch-offers-business"),
    path("api/offers-for-applications/fetch/", views.fetch_offers_for_applications, name="fetch-offers-for-applications"),
    path("api/offers/rate/", views.rate_offer, name="rate-offer"),
    path("api/offers/rate/cancel/", views.cancel_rate_offer, name="cancel-rate-offer"),
]
