from .views import HomepageView, TermsOfUseView, RuleAPIView
from django.urls import include, path

urlpatterns = [
    path('', HomepageView.as_view()),
    path('terms', TermsOfUseView.as_view()),
    path('rules', RuleAPIView.as_view(), name='rules-list')
]
