from django.urls import path
from apps.rule.views import RuleAPIView

urlpatterns = [
    path('', view=RuleAPIView.as_view(), name="rules"),
]
