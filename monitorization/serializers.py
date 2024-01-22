from rest_framework import serializers

from .models import Board, Workspace , InviteToWorkspace



class BoardChoiceSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Board
        fields = ("id", "title", "description", "workspace_id")



class WorkSpaceListSerializer(serializers.ModelSerializer):
    boards = BoardChoiceSerializer(many=True, read_only=True,source='board_set')
    class Meta:
        model = Workspace
        fields = ["id", "name", "description",'boards']




class WorkSpacePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description",'user']


class BoardListSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Board
        fields = ("id", "title", "description", "workspace_id")
        
        
class BoardPostSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Board
        fields = ("id", "title", "description", "workspace_id")
        
        
        
        
class InvitationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InviteToWorkspace
        fields = ['user',"workspace","token","is_accepted"]

