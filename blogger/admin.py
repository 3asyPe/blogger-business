from django.contrib import admin

from .models import (
    Blogger,
    BlogLanguage,
    BlogSpecialization,
)


admin.site.register(Blogger)
admin.site.register(BlogLanguage)
admin.site.register(BlogSpecialization)
