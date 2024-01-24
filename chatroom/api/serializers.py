from rest_framework import serializers
from ..models import Message
from accounts.serializer import UserSerializer




class MessageSerializer(serializers.ModelSerializer):
    sender=UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        
        
class MessageChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'