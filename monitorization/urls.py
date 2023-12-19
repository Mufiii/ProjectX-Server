from django.urls import path
from .views import (
       WorkSpaceListCreateAPiView,
       WorkSpaceGetUpdateAPIView,
       BoardListCreateView,
       BoardGetUpdateView
)     


urlpatterns = [

    path('workspace/',
          WorkSpaceListCreateAPiView.as_view(),
          name='workspace'
    ),
    path('workspace/<int:pk>/',
          WorkSpaceGetUpdateAPIView.as_view(),
          name='update_workspace'
    ),
    path('boards/',
          BoardListCreateView.as_view(),
          name='board'
    ),
    path('boards/<int:pk>/',
          BoardGetUpdateView.as_view(),
          name='update_board'
    )
]