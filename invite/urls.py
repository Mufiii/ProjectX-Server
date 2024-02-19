from django.urls import path
from .views import (
     InviteFreelancerstoProjectAPIView,
     DeveloperHiringAPIView
)


urlpatterns = [
    path('invite/',InviteFreelancerstoProjectAPIView.as_view(),name='invite'),
    path('hire/',DeveloperHiringAPIView.as_view(),name='hire')
]
