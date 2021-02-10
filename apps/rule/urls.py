from django.urls import path
from apps.rule.views import RuleView

urlpatterns = [
    path('', RuleView.as_view()),
]
