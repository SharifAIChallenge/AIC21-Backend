from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Resource, DownloadLink


class DownloadLinkInline(admin.StackedInline):
    model = DownloadLink


@admin.register(Resource)
class ResourceAdmin(ModelAdmin):
    inlines = (DownloadLinkInline,)


@admin.register(DownloadLink)
class DownloadLinkAdmin(ModelAdmin):
    pass
