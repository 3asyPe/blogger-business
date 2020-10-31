from django.urls import path

from . import views


app_name = "offer"


urlpatterns = [
    path("offers/", views.offers_view, name="list"),
    path("offers/actions/", views.offers_actions_view, name="actions"),
    path("offers/create/", views.offers_create_view, name="create"),
    path("api/offers/create/", views.create_offer, name="create-complete"),
]
