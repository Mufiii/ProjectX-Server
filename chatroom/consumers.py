from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.shortcuts import get_object_or_404
   
   
   

async def get_users_async(user_id):
    from accounts.models import User
    from accounts.serializer import UserSerializer
    
    user = await sync_to_async(get_object_or_404)(User, id=user_id)
    serializer = UserSerializer(user)
    return serializer.data

    
def save_message(message):
    from chatroom.api.serializer import MessageChannelSerializer
    
    serializer = MessageChannelSerializer(data=message)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data


class ChatConsumer(AsyncJsonWebsocketConsumer):
        
    async def connect(self):
        user = self.scope['user'].id
        self.user = await get_users_async(user)
        self.room_group_name = self.make_group_name(user)
        print(self.room_group_name)
        print(self.channel_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    def make_group_name(self, user_id):
        # Create a unique channel group name for the chat based on user ID
        return f"user_{user_id}"


    async def disconnect(self, close_code):
        print(f"WebSocket DISCONNECT issue: {close_code}")
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name, 
                self.channel_name
            )

    
    
    async def text_message(self, event):
    # Send the text message to the WebSocket clients in the group
        await self.send_json({
            'type':'text',
            "message":event
        })