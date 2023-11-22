from django.shortcuts import render
from .serializers import (
    DevProfileSerializer,DeveloperSerializer,
    ProjectViewSerializer
)
from vendor.serializer import ProjectProposalSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Developer
from accounts.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes,parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from vendor.models import Project,ProjectProposal
from django.shortcuts import get_object_or_404

class DevProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    
    def get(self,request,*args,**kwargs):
        serializer = DeveloperSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def put(self,request,*args,**kwargs):
        serializer = DeveloperSerializer(
        request.user, data=request.data , partial=True)
        if serializer.is_valid():
            user = User.objects.filter(id=request.user.id).first()
            # Here am Updating profile image
            instances = Developer.objects.filter(user=user).first()

            if 'profile_picture' in request.FILES:
                instances.profile_picture = request.FILES['profile_picture']

            if 'resume' in request.FILES:
                instances.resume = request.FILES['resume']

                instances.save()
            
                response_data = {
                    "msg": "Profile Updated Successfully",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
                
            user.save()
            serializer.save()
        
            return Response({"msg":"Data Updated", "data":serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class DevViewProjectAPIView(APIView):
    
    def get(self,request,pk=None):
        if pk is not None:
            projects = Project.objects.filter(id=pk)
        else:
            projects = Project.objects.all()
        if not projects:
            return Response(
                {'msg':"No Projects Found"},status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProjectViewSerializer(projects,many=True)
        return Response(
            serializer.data,status=status.HTTP_200_OK
        ) 
    
    
class DevProjectProposalView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    
    def get(self,request,project_id=None):
        try:
            project = Project.objects.get(id=project_id)
            serializer = ProjectViewSerializer(project)
            
            proposal_serializer = ProjectProposalSerializer()
            
            return Response({
                'project':serializer.data,
                'proposal':proposal_serializer.data
            }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request, project_id,format=None):
        project = get_object_or_404(Project, id=int(project_id))
        developer=User.objects.select_related("dev_profile").filter(id=request.user.id).first()

        serializer = ProjectProposalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            attachments_file = request.FILES.get("attachments")
            t=ProjectProposal.objects.create(
                project = project,
                developer=developer.dev_profile,
                cover_letter = serializer.validated_data.get("cover_letter"),
                notes = serializer.validated_data.get("notes"),
                approach = serializer.validated_data.get("approach"), 
                attachments = attachments_file,
                is_apply = True,
            )
                
            return Response(ProjectProposalSerializer(t).data, status=status.HTTP_201_CREATED)

        return Response({"errors": "There is an error"}, status=status.HTTP_400_BAD_REQUEST)
        
