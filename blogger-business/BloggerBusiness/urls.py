from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="home"),
    path('contact/', views.contact_view, name="contact"),
    path('about/', views.about_view, name="about"),
    path('terms-of-use/', views.terms_of_use_view, name="terms-of-use"),
    path('privacy-policy/', views.privacy_policy_view, name="privacy-policy"),
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