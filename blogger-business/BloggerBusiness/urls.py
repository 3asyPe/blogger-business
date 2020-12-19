from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from .views import (
    home_view,
    contact_view,
    about_view,
    terms_of_use_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('contact/', contact_view, name="contact"),
    path('about/', about_view, name="about"),
    path('terms-of-use/', terms_of_use_view, name="terms-of-use"),
    path('accounts/', include('account.passwords.urls')),
    path('', include('account.urls')),
    path('', include('application.urls')),
    path('', include('blogger.urls')),
    path('', include('business.urls')),
    path('', include('offer.urls')),
    path('', include('emails.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)