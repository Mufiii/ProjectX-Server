from django.urls import path
from .import views


urlpatterns = [
    path("vendorprofile/",
         views.VendorProfileView.as_view(), 
         name="vendorprofile"
    ),
    path("project/",
        views.ProjectListCreateAPIView.as_view(),
        name="project"
    ),
    path("project/<int:pk>/", 
        views.ProjectGetUpdateAPIView.as_view(), 
        name="project"
    ),
    path("applicationslist/<int:project_id>/",
          views.DeveloperApplicationsListAPIView.as_view(),
          name="applications",
    ),
    path("devfilter/<int:project_id>/<int:threshold_score>/",
        views.DeveloperSkillsMatchingAPIView.as_view(),
        name="devfilter",
    ),
    path(
        "skills/project_id/", 
        views.ProjectSkillsGetAPIView.as_view(), 
        name="devfilter"
    ),
]
