from django.urls import path

from apps.infra_gateway.views import SubmissionCallbackAPIView

app_name = 'team'

urlpatterns = [
    path('submission/<int:submission_id>', view=SubmissionCallbackAPIView.as_view(), name="update submission"),

]
