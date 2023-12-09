from django.urls import path
from .views import WorkSpaceListCreateAPiView,WorkSpaceGetUpdateAPIView


urlpatterns = [

    path('workspace/',
          WorkSpaceListCreateAPiView.as_view(),
          name='workspace'
    ),
    path('workspace/<int:pk>/',
          WorkSpaceGetUpdateAPIView.as_view(),
          name='update_workspace'
    )
]