from django.contrib import admin
from .models import (Artist,Track)
from .style_models import MainStyle,NavStyle,FooterStyle,CatalogStyle


admin.site.register(Artist)

class AdminTrack(admin.ModelAdmin):
    list_display = ["title", "artist", "genre","upload_date"]
    list_filter = ["artist","genre"]
admin.site.register(Track, AdminTrack)

# styling models
admin.site.register(MainStyle)
admin.site.register(NavStyle)
admin.site.register(FooterStyle)
admin.site.register(CatalogStyle)