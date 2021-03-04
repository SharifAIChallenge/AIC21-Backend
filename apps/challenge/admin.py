from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
#
from martor.widgets import AdminMartorWidget
from apps.challenge.models import ClanTeam, Clan


@admin.register(Clan)
class TeamAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass


@admin.register(ClanTeam)
class InvitationAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass


