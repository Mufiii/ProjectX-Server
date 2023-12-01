from django.urls import path
from developer import views
import uuid

urlpatterns = [
    path('profile/',
         views.DevProfileView.as_view(),
         name="profile"
    ),
    
    path('view_projects/',
         views.DevViewProjectAPIView.as_view(),
         name="view_projects"
    ),
    
    path('view_projects/<int:pk>/',
         views.DevViewProjectAPIView.as_view(),
         name="view_projects"
    ),
    
    path('view_projects/<int:project_id>/apply/',
         views.DevProjectProposalView.as_view(),
         name="view_projects"
    ),
    
    path('education/',
         views.DeveloperEducationListCreateApiView.as_view(),
         name="education"
    ),
    path('education/<int:pk>/',
         views.DeveloperEducationGetUpdateAPIView.as_view(),
         name="education"
    ),
]
