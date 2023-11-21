from django.urls import path
from .import views

urlpatterns = [
    path('profileee/',
         views.VendorProfileView.as_view(),
         name="vendorprofile"
    ),
    
    path('project/',
         views.ProjectListCreateAPIView.as_view(),
         name="project"
    ),
    
    path('project/<int:pk>/',
         views.ProjectGetUpdateAPIView.as_view(),
         name="project"
    ),
    
    path('applicationslist/',
         views.DeveloperApplicationsListAPIView.as_view(),
         name="applications"
    ),
    
]
