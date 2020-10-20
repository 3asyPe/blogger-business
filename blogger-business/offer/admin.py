from django.contrib import admin

from .models import (
    Offer,
    BloggerModel,
    BloggersRate,
    BloggerModelLanguage,
    BloggerModelSpecialization,
)


admin.site.register(Offer)
admin.site.register(BloggerModel)
admin.site.register(BloggersRate)
admin.site.register(BloggerModelLanguage)
admin.site.register(BloggerModelSpecialization)
