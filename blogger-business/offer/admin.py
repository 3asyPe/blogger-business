from django.contrib import admin

from .models import (
    Offer,
    BloggerModel,
    BloggerModelLanguage,
    BloggerModelSpecialization,
    BloggerModelAgeGroup,
)


admin.site.register(Offer)
admin.site.register(BloggerModel)
admin.site.register(BloggerModelLanguage)
admin.site.register(BloggerModelSpecialization)
admin.site.register(BloggerModelAgeGroup)
