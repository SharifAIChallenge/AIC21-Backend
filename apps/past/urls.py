from django.urls import path
from apps.past.views import PastListAPIView, PastInstanceAPIView

urlpatterns = [
    path('', view=PastListAPIView.as_view(), name="all_past_ai"),
    path('<int:past_id>', view=PastInstanceAPIView.as_view(), name="single_past_ai")
]

