


from django .urls import path
from chatroom.views import ChatRoomView , MessageView

urlpatterns = [
    path('chats', ChatRoomView.as_view(), name='chatRoom'),
    path('chats/<str:roomId>/messages', MessageView.as_view(), name='messageList'),
	path('users/<int:userId>/chats', ChatRoomView.as_view(), name='chatRoomList'),
]
