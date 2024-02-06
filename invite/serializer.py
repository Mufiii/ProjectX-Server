from rest_framework import serializers
from .models import Invitation
from accounts.models import User
from vendor. models import Project

class InvitationSerializer(serializers.Serializer):
    project = serializers.IntegerField()
    user = serializers.IntegerField()
    message = serializers.CharField()

    def create(self, validated_data):
        project_id = validated_data.get('project')
        user_id = validated_data.get('user')
        message = validated_data.get('message')

        project = Project.objects.get(id=project_id)
        user = User.objects.get(id=user_id)

        invite = Invitation.objects.create(
            user=user,
            project=project,
            message=message,
            is_invited=True
        )
        
        return invite