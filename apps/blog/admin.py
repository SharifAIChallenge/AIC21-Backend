from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from martor.widgets import AdminMartorWidget

from apps.blog.models import Post, Comment, Tag, AparatMedia


class AparatInline(admin.StackedInline):
    model = AparatMedia


@admin.register(Post)
class PostAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    inlines = (AparatInline,)
    list_display = ('id', 'title_fa', 'google_calendar_link', 'webinar_link')
    list_editable = ('google_calendar_link', 'webinar_link')


@admin.register(AparatMedia)
class AparatMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    comment_shown_editable = ['shown']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass
