from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *


# class MytokenSerializer(TokenObtainPairSerializer):
#     # transform a method into a class method
#     @classmethod
#     def get_token(cls, obj, *args):
#         token = super().get_token(obj)
#         if obj.id:
#             token["user_id"] = obj.id
#         if obj.email:
#             token["email"] = obj.email
#         if obj.username is not None:
#             token["username"] = obj.username
#         if obj.is_developer:
#             token["is_developer"] = True
#         if obj.is_vendor:
#             token["is_vendor"] = True
#         return token

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
