from django.urls import path

from . import views

app_name = 'faq'

urlpatterns = [
    path('questions/', views.FaqsAPIView.as_view(), name='questions_list')
]
