from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.accounts.models import Profile
from apps.challenge.models import Match
from apps.homepage.serializers import SubscribeSerializer
from apps.staff.models import Staff
from apps.staff.serializers import StaffSerializer
from apps.team.models import Submission, Team
from .models import Intro, TimelineEvent, Prize, Stats, Sponsor, WhyThisEvent, \
    Quote, Motto, Media, SocialMedia, Rule, GoogleAddEventToCalender

from .serializers import IntroSerializer, TimelineEventSerializer, \
    PrizeSerializer, StatSerializer, \
    SponsorSerializer, WhyThisEventSerializer, QuoteSerializer, \
    MottoSerializer, MediaSerializer, SocialMediaSerializer, \
    RuleSerializer


class TimelineView(GenericAPIView):

    def get(self, request):
        url = ''
        if GoogleAddEventToCalender.objects.all().last():
            url = GoogleAddEventToCalender.objects.all().last().url
        data = {
            'data': TimelineEventSerializer(
                TimelineEvent.objects.all().order_by('id').order_by('order'),
                many=True).data,
            'calendar': url
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

    def get(self, request, sponsor_title):
        queryset = Sponsor.objects.all()
        data = {
            'data': SponsorSerializer(queryset, many=True).data
        }
        if sponsor_title != 'all':
            queryset = queryset.filter(title_en=sponsor_title).last()
            data['data'] = SponsorSerializer(queryset).data

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
            'data': StaffSerializer(Staff.objects.all().order_by('?')[:8],
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
            'data': [{
                'title': 'نبرد',
                'icon': 'mdi-sword-cross',
                'stat': Match.objects.count(),
            }, {
                'title': 'ارسال کد',
                'icon': 'mdi-code-braces-box',
                'stat': Submission.objects.count(),
            }, {
                'title': 'تیم',
                'icon': 'mdi-account-group',
                'stat': Team.objects.count(),
            }, {
                'title': 'شرکت‌کننده',
                'icon': 'mdi-clipboard-account',
                'stat': Profile.objects.count(),
            },

            ]
        }
        return Response(data)


class SocialsView(GenericAPIView):

    def get(self, request):
        data = {
            'socials': SocialMediaSerializer(SocialMedia.objects.all(),
                                             many=True).data
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


class SubscribeAPIView(GenericAPIView):
    serializer_class = SubscribeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            data={'details': 'Subscribed'},
            status=status.HTTP_200_OK
        )
