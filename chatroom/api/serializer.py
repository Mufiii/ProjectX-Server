from rest_framework import serializers
from chatroom.models import ChatMessage , ChatRoom
from accounts.serializer import UserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True, read_only=True)
    members = serializers.ListField(write_only=True)
    
    class Meta :
        model = ChatRoom
        exclude = ['id']
        
    def create(self,validated_data):
        memberObject = validated_data.pop('members')
        chatroom = ChatRoom.objects.create(**validated_data)
        chatroom.member.set(memberObject)
        return chatroom
    
    
class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        exclude = ['id','chat']
        
    def get_userName(self, Obj):
        return Obj.user.first_name + ' ' + Obj.user.last_name
        