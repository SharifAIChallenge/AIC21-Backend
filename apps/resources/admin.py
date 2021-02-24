from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Resource, DownloadLink


# Register your models here.

@admin.register(Resource)
class ResourceAdmin(ModelAdmin):
    pass


@admin.register(DownloadLink)
class DownloadLinkAdmin(ModelAdmin):
    pass
