from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class MytokenSerializer(TokenObtainPairSerializer):
    # transform a method into a class method
    @classmethod
    def get_token(cls,obj, *args):
        token = super().get_token(obj)
        if obj.id:
            token["user_id"] = obj.id
        if obj.email:
            token["email"] = obj.email
        if obj.username is not None:
            token['username'] = obj.username
        return token
        

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'country'
        ]
    
    


class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'country'
        ]
        

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
             