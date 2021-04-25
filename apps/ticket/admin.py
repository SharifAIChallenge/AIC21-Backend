from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from martor.widgets import AdminMartorWidget

from apps.ticket.models import Tag
from apps.ticket.models import Ticket, Reply


class ReplyInline(admin.StackedInline):
    model = Reply


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    list_display = ('id', 'author', 'tag', 'title', 'status')

    list_filter = ('tag', 'status')
    search_fields = ('id',)

    inlines = (ReplyInline,)


@admin.register(Reply)
class ReplyAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    list_display = ('id', 'user', 'status')
    list_filter = ('status',)
    search_fields = ('id',)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('id',)
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass
