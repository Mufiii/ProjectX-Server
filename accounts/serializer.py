from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *


class MytokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, *args):
        token = super().get_token(user)

        # Include additional user information in the token payload
        token["user_id"] = user.id
        token["email"] = user.email
        token["username"] = user.username
        token["is_developer"] = user.is_developer
        token["is_vendor"] = user.is_vendor

        return token



class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "username", "last_name", "email", "country"]


class DeveloperChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "username", "last_name", "email", "country"]


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "country"]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "username", "last_name", "email", "country"]