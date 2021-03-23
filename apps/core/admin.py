from django.contrib import admin

from rest_framework_tracking.admin import APIRequestLogAdmin as BaseLogAdmin

# Register your models here.
from apps.core.models import APIRequestLogProxy


@admin.register(APIRequestLogProxy)
class APIRequestLogProxyAdmin(BaseLogAdmin):
    list_filter = ('method', 'path', 'status_code')
