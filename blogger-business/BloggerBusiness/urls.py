"""BloggerBusiness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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
    path('', include('account.urls')),
    path('', include('application.urls')),
    path('', include('blogger.urls')),
    path('', include('business.urls')),
    path('', include('offer.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)