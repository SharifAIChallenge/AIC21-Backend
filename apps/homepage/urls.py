from .views import *
from django.urls import include, path

urlpatterns = [
    path('timeline', TimelineView.as_view()),
    path('prizes', PrizesView.as_view()),
    path('Sponsers', SponsorsView.as_view()),
    path('why', WhyView.as_view()),
    path('staffs', StaffsView.as_view()),
    path('stat', StatView.as_view()),
    path('socials', SocialsView.as_view()),
    path('motto', MottoView.as_view()),
    path('intro', IntroView.as_view()),
    path('quotes', QuotesView.as_view()),
    path('terms', TermsOfUseView.as_view()),
    path('rules', RuleAPIView.as_view(), name='rules-list')
]
