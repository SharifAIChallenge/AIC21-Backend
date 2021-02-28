from django.conf import settings

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import Intro, TimelineEvent, Prize, Stats, Sponsor, WhyThisEvent, \
    Quote, Motto, Media, SocialMedia, Rule, Subscribe


class IntroSerializer(ModelSerializer):
    class Meta:
        model = Intro
        exclude = ['id']


class TimelineEventSerializer(ModelSerializer):
    class Meta:
        model = TimelineEvent
        exclude = ['id']


class PrizeSerializer(ModelSerializer):
    class Meta:
        model = Prize
        exclude = ['id']


class StatSerializer(ModelSerializer):
    class Meta:
        model = Stats
        exclude = ['id']


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        exclude = ['id']


class WhyThisEventSerializer(ModelSerializer):
    class Meta:
        model = WhyThisEvent
        exclude = ['id']


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quote
        exclude = ['id']


class MottoSerializer(ModelSerializer):
    class Meta:
        model = Motto
        exclude = ['id']


class MediaSerializer(ModelSerializer):
    file = serializers.SerializerMethodField('_get_file')

    @staticmethod
    def _get_file(obj: Media):
        url = obj.file.url
        if settings.DOMAIN not in url:
            return settings.DOMAIN + url
        return url

    class Meta:
        model = Media
        fields = ['title', 'file']


class SocialMediaSerializer(ModelSerializer):
    class Meta:
        model = SocialMedia
        exclude = ['id']


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['title_en', 'title_fa', 'text_en', 'text_fa', 'order']


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('email',)
