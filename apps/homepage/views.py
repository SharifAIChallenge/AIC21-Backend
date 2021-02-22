from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.staff.models import Staff
from apps.staff.serializers import StaffSerializer
from .models import Intro, TimelineEvent, Prize, Stat, Sponsor, WhyThisEvent, \
    Quote, Motto, Media, SocialMedia
from .serializers import IntroSerializer, TimelineEventSerializer, \
    PrizeSerializer, StatSerializer, \
    SponsorSerializer, WhyThisEventSerializer, QuoteSerializer, MottoSerializer, MediaSerializer, SocialMediaSerializer, \
    Quote, RuleSerializer, Rule


class TimelineView(GenericAPIView):

    def get(self, request):
        data = {
            'data': TimelineEventSerializer(
                TimelineEvent.objects.all().order_by('id').order_by('order'),
                many=True).data
        }
        return Response(data)


class PrizesView(GenericAPIView):

    def get(self, request):
        data = {
            'data': PrizeSerializer(Prize.objects.all().order_by('id'),
                                      many=True).data
        }
        return Response(data)


class SponsorsView(GenericAPIView):

    def get(self, request):
        data = {
            'data': SponsorSerializer(Sponsor.objects.all(),
                                          many=True).data
        }
        return Response(data)


class WhyView(GenericAPIView):

    def get(self, request):
        data = {
            'data': WhyThisEventSerializer(WhyThisEvent.objects.all(),
                                          many=True).data
        }
        return Response(data)


class QuotesView(GenericAPIView):

    def get(self, request):
        data = {
            'data': QuoteSerializer(Quote.objects.all(), many=True).data
        }
        return Response(data)


class StaffsView(GenericAPIView):

    def get(self, request):
        data = {
            'data': StaffSerializer(Staff.objects.all().order_by('?')[:5],
                                      many=True).data
        }
        return Response(data)


class MediaView(GenericAPIView):

    def get(self, request):
        data = {
            'data': MediaSerializer(Media.objects.all(), many=True).data
        }
        return Response(data)


class StatView(GenericAPIView):

    def get(self, request):
        data = {
            'data': StatSerializer(Stat.objects.all(), many=True).data
        }
        return Response(data)


class SocialsView(GenericAPIView):

    def get(self, request):
        data = {
            'socials': SocialMediaSerializer(SocialMedia.objects.all(), many=True).data
        }
        return Response(data)


class MottoView(GenericAPIView):

    def get(self, request):
        data = {
            'data': MottoSerializer(Motto.objects.all(), many=True).data
        }
        return Response(data)


class IntroView(GenericAPIView):

    def get(self, request):
        data = {
            'data': IntroSerializer(Intro.objects.last()).data
        }
        return Response(data)


class TermsOfUseView(GenericAPIView):

    def get(self, request):
        data = {
            'data': Intro.objects.first().term_of_use
        }
        return Response(data)


class RuleAPIView(GenericAPIView):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all().order_by('order')

    def get(self, request):
        rules = self.get_serializer(self.get_queryset(), many=True)
        return Response(data={"data": rules.data}, status=status.HTTP_200_OK)
