from django.urls import path , include
from rest_framework import routers
from .views import (
    BoardGetUpdateView,
    BoardListCreateViewset,
    WorkSpaceGetUpdateAPIView,
    WorkSpaceListCreateAPiView,
    WorkspaceInviteViewset,
    ListViewset,
    CardViewset
)

router = routers.DefaultRouter()
router.register(r'lists', ListViewset)
router.register(r'cards', CardViewset)

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
         WorkspaceInviteViewset.as_view(),
         name='invite'
    ),
    
    path('', include(router.urls)),
    
     # path('lists/', ListViewset.as_view({'get': 'list', 'post': 'create'}), name='lists'),
     # path('lists/<int:pk>/', ListViewset.as_view({'get': 'retrieve'}), name='list_detail'),


]                       
