from .views import ResourceAPIView
from django.urls import path

urlpatterns = [
    path('', ResourceAPIView.as_view()),
]