from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from .models import Board, Workspace , List , Card
from rest_framework.decorators import action
from .serializers import (
    BoardListSerializer,
    BoardPostSerializer,
    WorkSpaceListSerializer,
    WorkSpacePostSerializer,
    ListsSerializer,
    CardsSerializer
)
from .utils.generate_token import generate_unique_token
from accounts.models import User
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils.InviteEmail import Invitation_send_email


class WorkSpaceListCreateAPiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        worksapce = Workspace.objects.filter(user=request.user)
        serializer = WorkSpaceListSerializer(worksapce, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkSpaceListSerializer(data=request.data)
        if serializer.is_valid():
            workspace = Workspace.objects.create(
                user=request.user,
                name=serializer.validated_data["name"],
                description=serializer.validated_data["description"],
            )
            workspace.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WorkSpaceGetUpdateAPIView(APIView):
    def get(self, request, pk):
        try:
            workspace = Workspace.objects.prefetch_related('board').get(pk=pk)  
            print(workspace)                          
            serializer = WorkSpaceListSerializer(workspace)                         
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Workspace.DoesNotExist:
            return Response(
                {"error": "Workspace not found"}, status=status.HTTP_404_NOT_FOUND
            )
            

    def put(self, request, pk):
        workspace = Workspace.objects.get(pk=pk, user=request.user.id)
        print(workspace)
        serializer = WorkSpacePostSerializer(workspace, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"msg": "There is an error"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        workspace = Workspace.objects.get(pk=pk, vendor__user__id=request.user.id)
        workspace.delete()
        return Response(
            {"msg": "Workspace deleted Successfully"}, status=status.HTTP_200_OK
        )

class BoardListCreateViewset(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    
    @action(detail=True, methods=['post'])
    def post(self, request, *args, **kwargs):
        q = request.query_params.get('q')
        print(q)
        if q:
            try:
                workspace = Workspace.objects.get(id=q)
                board_data = {
                    "workspace_id": workspace.id,  
                    "title": request.data.get("title"),
                    "description": request.data.get("description"),
                }
                print(board_data)  # Check the values in board_data
                
                serializer = BoardPostSerializer(data=board_data)
                
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print(serializer.data, 'Data saved successfully')
                    return Response(serializer.data, status=201)
                else:
                    print(serializer.errors, 'Serializer errors')
                    return Response(serializer.errors, status=400)
            except Workspace.DoesNotExist:
                return Response({"error": "Workspace not found"}, status=404)
        else:
            return Response({"error": "Workspace ID (q) is required"}, status=400)
        
        
    def list(self,request, *args,**kwargs):
        user = self.request.user
        board =  Board.objects.select_related('workspace__user').filter(workspace__user=user)
        serializer = BoardListSerializer(board,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

            


class BoardGetUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer



class WorkspaceInviteViewset(APIView):
    
    def post(self, request, workspace_id, *args, **kwargs):
        
        user_email = request.data.get('email')
        
        try:
            workspace = Workspace.objects.filter(short_name=workspace_id).select_related('user').first()

            if workspace:
                token = generate_unique_token()

                current_site = "localhost:5173"
                relative_link = reverse('invite', kwargs={'workspace_id': workspace.short_name})
                absurl = f"http://{current_site}{relative_link}{str(token)}"

                email_body = (
                    f"{workspace.user.first_name} {workspace.user.last_name} "
                    f"invited you to their Workspace {workspace.name}.\n\n"
                    "Join them on Trello to collaborate, manage projects, and reach new productivity peaks.\n" 
                    f"{absurl}"
                )
                

                data = {
                    "email_body": email_body,
                    "to_email": user_email,
                    "email_subject": "Invitation",
                    "from_email": workspace.user.email
                }
                
                Invitation_send_email(data)

                return Response(
                    {"data":data,"Invitation_link": absurl}, status=status.HTTP_200_OK )
            else:
                return Response(
                    {"error": "Workspace not found."},
                            status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

                

class ListViewset(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListsSerializer
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
            'message': 'List created successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    

class CardViewset(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardsSerializer
    
    def create(self, request, *args, **kwargs):
        list_column_id = request.data.get('list_column_id')
        if not list_column_id:
            return Response({'error': 'list_column_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            list_instance = List.objects.get(id=list_column_id)
        except List.DoesNotExist:
            return Response({'error': 'List does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Modify the field name in the request data
        request.data['list_column'] = list_column_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set the list_column to the associated list
        serializer.validated_data['list_column'] = list_instance
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
