from django.contrib import admin
from apps.past.models import Past
from django.contrib.admin import ModelAdmin
from django.db import models
from martor.widgets import AdminMartorWidget


# Register your models here.

@admin.register(Past)
class PastAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    list_display = ('id', 'event_year')
