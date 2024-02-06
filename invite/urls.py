from django.urls import path
from .views import InviteFreelancerstoProjectAPIView

urlpatterns = [
    path('invite/',InviteFreelancerstoProjectAPIView.as_view(),name='invite')
]
