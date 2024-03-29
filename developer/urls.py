import uuid

from django.urls import path

from developer import views

urlpatterns = [
    path("profile/", 
         views.DevProfileView.as_view(),
         name="profile"
    ),
    path("view_projects/", 
         views.DevViewProjectAPIView.as_view(), 
         name="view_projects"
    ),
    path(
        "view_projects/<int:pk>/",
        views.DevViewProjectAPIView.as_view(),
        name="view_projects",
    ),
    path(
        "view_projects/<int:project_id>/apply/",
        views.DevProjectProposalView.as_view(),
        name="view_projects",
    ),
    path(
        "education/",
        views.DeveloperEducationListCreateApiView.as_view(),
        name="key_education",
    ),
    path(
        "education/<int:pk>/",
        views.DeveloperEducationGetUpdateAPIView.as_view(),
        name="education",
    ),
    path(
        "experience/",
        views.DevExperienceListCreateAPIView.as_view(),
        name="key_experience",
    ),
    path(
        "experience/<int:pk>/",
        views.DevExperienceGetUpdateAPIView.as_view(),
        name="experience",
    ),
    path("skills/", 
         views.SkillsListUpdatingAPIView.as_view(), 
         name="skills"
    ),
]
