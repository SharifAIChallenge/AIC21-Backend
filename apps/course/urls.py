from django.conf.urls import url
from django.urls import path

from apps.course.views import *

urlpatterns = [
    path('', CourseView.as_view()),
]
