from django.contrib import admin
from .models import ImageLink, ThumbImage


class ImageLinkAdmin(admin.ModelAdmin):
    fields = ['image', 'expiry_time']

admin.site.register(ImageLink, ImageLinkAdmin)


class ThumbImageAdmin(admin.ModelAdmin):
    fields = ['created', 'owner']

admin.site.register(ThumbImage, ThumbImageAdmin)