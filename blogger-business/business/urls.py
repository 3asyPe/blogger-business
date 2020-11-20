from django.urls import path

from . import views


app_name = "business"


urlpatterns = [
    path("api/business-profile-data/info/", views.fetch_business_info_profile_data, name="fetch-business-info-profile-data"),
    path("api/business-profile-data/info/edit/", views.edit_business_info_profile_data, name="edit-business-info-profile-data"),
    path("api/business-profile-data/contact/", views.fetch_business_contact_profile_data, name="fetch-business-contact-profile-data"),
    path("api/business-profile-data/contact/edit/", views.edit_business_contact_profile_data, name="edit-business-contact-profile-data"),
]
