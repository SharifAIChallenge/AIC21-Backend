from django.urls import path
from apps.past.views import PastView

urlpatterns = [
    path('', PastView()),
]
