from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import (
    BoardGetUpdateView,
    BoardListCreateViewset,
    WorkSpaceGetUpdateAPIView,
    WorkSpaceListCreateAPiView,
    WorkspaceInviteViewset
)

# router = DefaultRouter()
# router.register(r'invite', WorkspaceInviteLink, basename='workspace-invites')

urlpatterns = [
    path("workspace/", 
         WorkSpaceListCreateAPiView.as_view(), 
         name="workspace"
    ),
    path(
        "workspace/<int:pk>/",
        WorkSpaceGetUpdateAPIView.as_view(),
        name="update_workspace",
    ),
    path("boards/", 
        BoardListCreateViewset.as_view(
             {'get': 'list', 'post': 'post'}
        ),
         name="board"
    ),
    path("boards/<int:pk>/", 
         BoardGetUpdateView.as_view(), 
         name="update_board"
    ),
    path('invite/<str:workspace_id>/', 
         WorkspaceInviteViewset.as_view({'post':'post'}), 
         name='invite'
    ),

]                       
