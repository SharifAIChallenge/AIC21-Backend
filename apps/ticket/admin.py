from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from martor.widgets import AdminMartorWidget

from apps.ticket.models import Ticket,Reply


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass


@admin.register(Reply)
class ReplyAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass

