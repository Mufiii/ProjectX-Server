from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
import asyncio


def get_users_async(user_id):
    from accounts.models import User
    from accounts.serializer import UserSerializer

    try:
        the_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        the_user = None

    serializer = UserSerializer(data=the_user)
    serializer.is_valid(raise_exception=True)
    return serializer.data

    
@database_sync_to_async
def save_message(message:dict):
    from chatroom.models import Message
    from chatroom.api.serializers import MessageChannelSerializer
    
    serializer = MessageChannelSerializer(data=message)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data

class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.user = None
    
    
    async def connect(self):
        if not self.scope['user'].is_anonymous:
            self.user = self.scope['user']
            user = get_users_async(self.user.id)
            self.room_group_name = self.make_group_name()
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close(code=1009)
            return
        
    async def receive_json(self, content):
        message_type = content.get('type')
        if message_type == 'text':
            # Handle text message
            await self.handle_text_message(content)
        elif message_type == 'audio':
            # Handle audio file
            await self.handle_file_message(content, 'audio')
        elif message_type == 'video':
            # Handle video file
            await self.handle_file_message(content, 'video')
            
    # async def handle_text

    # def disconnect(self, close_code):
    #     # Leave room group
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    # def receive(self, text_data):
    #     # Receive message from WebSocket
    #     text_data_json = json.loads(text_data)
    #     text = text_data_json['text']
    #     sender = text_data_json['sender']
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': text,
    #             'sender': sender
    #         }
    #     )

    # def chat_message(self, event):
    #     # Receive message from room group
    #     text = event['message']
    #     sender = event['sender']
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         'text': text,
    #         'sender': sender
    #     }))