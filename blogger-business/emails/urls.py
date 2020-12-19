from django.urls import path

from . import views


app_name = "emails"


urlpatterns = [
    path("email/activate/<str:key>", views.email_activation_view, name="activate-email"),
    path("api/email/reactivate/", views.email_reactivation, name="reactivate-email"),
]
