from django.urls import path

from apps.infra_gateway.views import UpdateSubmissionAPIView

app_name = 'team'

urlpatterns = [
    path('submission/<int:submission_id>', view=UpdateSubmissionAPIView.as_view(), name="update submission"),

]
