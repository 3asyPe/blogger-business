from django.contrib import admin

from .models import (
    Youtube, 
    YoutubeStatistics,
    YoutubeAudience,
)


admin.site.register(Youtube)
admin.site.register(YoutubeStatistics)
admin.site.register(YoutubeAudience)
