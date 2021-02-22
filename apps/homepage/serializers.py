from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import Intro, TimelineEvent, Prize, Stats, Sponsor, WhyThisEvent, Quote, Motto, Media, SocialMedia, Rule


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
    class Meta:
        model = Media
        exclude = ['id']


class SocialMediaSerializer(ModelSerializer):
    class Meta:
        model = SocialMedia
        exclude = ['id']


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['title_en', 'title_fa', 'text_en', 'text_fa', 'order']
