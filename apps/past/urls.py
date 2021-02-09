from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from apps.past.views import PastView


router = DefaultRouter()
router.register('', PastView)
router.register('/<int:pk>', PastView)

urlpatterns = []
urlpatterns += router.urls