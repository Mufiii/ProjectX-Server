from rest_framework import serializers
from .models import Workspace , Board


class WorkSpaceListSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Workspace
        fields = ['id','name','description']
        
        
class WorkSpacePostSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'vendor']
        
        
class BoardListSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Board
        fields = ('id','title','description','workspace_id')
        
    def create(self, validated_data):
        # Extract the workspace_id from the validated data
        workspace_id = validated_data.pop('workspace_id', None)
        workspace = Workspace.objects.get(id=workspace_id)
        # Create the Board instance and associate it with the Workspace
        board = Board.objects.create(workspace=workspace, **validated_data)

        return board
        
        
class BoardPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Board
        fields = ['id','title','description']
        
    