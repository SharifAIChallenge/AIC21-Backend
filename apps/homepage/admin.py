from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from martor.widgets import AdminMartorWidget

from apps.homepage.models import Subscribe
from .models import Intro, TimelineEvent, Prize, Stats, Sponsor, WhyThisEvent, \
    Quote, Motto, Media, SocialMedia, Rule, GoogleAddEventToCalender


@admin.register(Intro)
class IntroAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(TimelineEvent)
class TimelineEventAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Prize)
class PrizeAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Stats)
class StatsAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Sponsor)
class SponsorAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(WhyThisEvent)
class WhyThisEventAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Quote)
class QuoteAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Motto)
class MottoEventAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Media)
class MediaEventAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(SocialMedia)
class SocialMediaEventAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Rule)
class RuleAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    pass


@admin.register(GoogleAddEventToCalender)
class GoogleAddEventToCalender(ModelAdmin):
    list_display = ('id', 'url',)
    list_editable = ('url',)
    sortable_by = ('id', 'url')


@admin.register(Subscribe)
class SubscribeAdmin(ModelAdmin):
    list_display = ('id', 'email')
    list_display_links = ('id',)
