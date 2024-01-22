from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class MytokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, *args):
        
        token = RefreshToken.for_user(user)
        
        # Include additional user information in the token payload
        token["user_id"] = user.id
        token["email"] = user.email
        token["username"] = user.username
        token["is_developer"] = user.is_developer
        token["is_vendor"] = user.is_vendor

        return token

