from rest_framework import serializers

from .models import Board, Workspace , List , Card



class BoardChoiceSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Board
        fields = ("id", "title", "description", "workspace_id")



class WorkSpaceListSerializer(serializers.ModelSerializer):
    board = BoardChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Workspace
        fields = ["id", "name", "description",'board']




class WorkSpacePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description",'user']

class ListsChoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = List
        fields = ('id','list_title',)


class BoardListSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)
    lists = ListsChoiceSerializer(many=True)
    
    class Meta:
        model = Board
        fields = ("id", "title", "description", "workspace_id",'lists')
        
        
class BoardPostSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Board
        fields = ("id", "title", "description", "workspace_id")
        

class CardChoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card
        fields = ('id','card')
        
        
class ListsSerializer(serializers.ModelSerializer):
    cards = CardChoiceSerializer(many=True, required=False)
    board = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = List
        fields = ('id', 'list_title', 'board','cards')
        read_only_fields = ('cards',)

    def validate_board(self, value):
        try:
            board = Board.objects.get(pk=value)
            print(board,'22222222')
            return board
        except Board.DoesNotExist:
            raise serializers.ValidationError("Invalid board_id")
        
        
        
class CardsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card
        fields = ('id','card','list_column')