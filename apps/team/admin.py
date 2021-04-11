from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from martor.widgets import AdminMartorWidget

from apps.team.models import Team, Invitation, Submission


class SubmissionInline(admin.StackedInline):
    model = Submission


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    list_display = ('id', 'name', 'image', 'creator', 'level_one_payed')
    inlines = (SubmissionInline,)


@admin.register(Invitation)
class InvitationAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    pass
