import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from chatroom.models import ChatMessage,ChatRoom ,OnlineUser
from accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    
        def getUser(self,userId):
            return User.objects.get(id=userId)

        def getOnlineUsers(self):
            onlineUsers = OnlineUser.objects.all()
            return [onlineUser.user.id for onlineUser in onlineUsers]


        def addOnlineUser(self, user):
            try:
                OnlineUser.objects.create(user=user)
            except:
                pass

        def deleteOnlineUser(self, user):
            try:
                OnlineUser.objects.get(user=user).delete()
            except:
                pass
            
            
        def saveMessage(self,message,userId,roomId):
            userObj = User.objects.get(id=userId)
            chatObj = ChatRoom.objects.get(roomId=roomId)
            chatMessageObj = ChatMessage.objects.create(
                chat=chatObj, user=userObj, message=message
            )
            return {
                'action':'message',
                'user':'userId',
                'roomId': roomId,
                'message': message,
                'username':  userObj.username ,
                'timestamp': str(chatMessageObj.timestamp)
            }
            
            
            
        async def sendOnlineUserList(self):
            onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
            chatMessage = {
                'type': 'chat_message',
                'message': {
                    'action': 'onlineUser',
                    'userList': onlineUserList
                }
            }
            await self.channel_layer.group_send('onlineUser', chatMessage)

            
        # connect    
        async def connect(self):
            print(self.scope)
            self.userId = self.scope['url_route']['kwargs']['userId']
            print(self.userId,'222')
            self.userRooms = await database_sync_to_async(
                list
            )(ChatRoom.objects.filter(member=self.userId))
            for room in self.userRooms:
                await self.channel_layer.group_add(
                    room.roomId,
                    self.channel_name
                )
            await self.channel_layer.group_add('onlineUser', self.channel_name)
            self.user = await database_sync_to_async(self.getUser)(self.userId)
            await database_sync_to_async(self.addOnlineUser)(self.user)
            await self.sendOnlineUserList()
            await self.accept()
            
            
        # disconnect    
        async def disconnect(self,close_code):
            await database_sync_to_async(self.deleteOnlineUser)(self.user)
            await self.sendOnlineUserList()
            for room in self.userRooms:
                await self.channel_layer.group_discard(
                    room.roomId,
				    self.channel_name
                )
        
        
                
        # recieve
        async def recieve(self,text_data):
            text_data_json = json.loads(text_data)
            action = text_data_json['action']
            roomId = text_data_json['roomId']
            chatMessage = {}
            if action == 'message':
                message = text_data_json['message']
                userId = text_data_json['user']
                chatMessage = await database_sync_to_async(
                    self.saveMessage
                )(message, userId, roomId)
            elif action == 'typing':
                chatMessage = text_data_json
            await self.channel_layer.group_send(
                roomId,
                {
                    'type': 'chat_message',
                    'message': chatMessage
                }
            )
        
            

        async def chat_message(self, event):
            message = event['message']
            await self.send(text_data=json.dumps(message))
            
            
            
            
            
            
# async def get_users_async(user_id):
#     from accounts.models import User
#     from accounts.serializer import UserSerializer
    
#     user = await sync_to_async(get_object_or_404)(User, id=user_id)
#     print(user,'777')
#     serializer = UserSerializer(user)
#     print(serializer.data,'666')
#     return serializer.data

    
# def save_message(message):
#     from chatroom.api.serializer import MessageChannelSerializer
    
#     serializer = MessageChannelSerializer(data=message)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
    
#     return serializer.data


# class ChatConsumer(AsyncJsonWebsocketConsumer):
        
#     async def connect(self):
#         # print(self.scope,'0000')
#         user = self.scope['user'].id
#         self.user = await get_users_async(user)
#         self.room_group_name = self.make_group_name(user)
#         print(self.room_group_name,'222')
#         print(self.channel_name,'333')
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     def make_group_name(self, user_id):
#         return f"user_{user_id}"


#     async def disconnect(self, close_code):
#         print(f"WebSocket DISCONNECT issue: {close_code}")
#         if self.room_group_name:
#             await self.channel_layer.group_discard(
#                 self.room_group_name, 
#                 self.channel_name
#             )

    
    
#     async def text_message(self, event):
#     # Send the text message to the WebSocket clients in the group
#         await self.send_json({
#             'type':'text',
#             "message":event
#         })