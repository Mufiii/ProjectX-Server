from rest_framework import serializers
from .models import Workspace


class WorkSpaceListSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Workspace
        fields = ['id','name','description']
        
        
class WorkSpacePostSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'vendor']