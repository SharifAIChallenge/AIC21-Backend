from django.urls import path

from apps.infra_gateway.views import InfraEventPushAPIView

app_name = 'infra_gateway'

urlpatterns = [
    path(
        route='event/push',
        view=InfraEventPushAPIView.as_view(),
        name="update submission"
    ),

]
