from .serializer import (
    VendorProfileSerializer,
    VendorSerializer,
    ProjectSerializer,
    ProjectProposalSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

class VendorProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    
    def get(self,request):
        serializer = VendorSerializer(request.user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
      
    def put(self,request):
      serializer = VendorSerializer(
        request.user , data= request.data, partial=True
      )
      if serializer.is_valid():
          user = User.objects.filter(id=request.user.id).first()
          
          instances = BusinessVendor.objects.filter(user=user).first()
          
          if 'logo' in request.FILES:
              instances.logo = request.FILES['logo']
            
          if 'banner' in request.FILES:
              instances.banner = request.FILES['banner']
              
              instances.save()
            
              response_data = {
                      "msg": "Logo Updated Successfully",
                      "data": serializer.data
                  }
              return Response(response_data, status=status.HTTP_200_OK)
          
          user.save()
          serializer.save()
          
          return Response(serializer.data,status=status.HTTP_200_OK)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
              
              
          
class ProjectListCreateAPIView(APIView):
    authentication_classes=(JWTAuthentication,)
    permission_classes=(IsAuthenticated,)
    
    def get(self,request):
        projects = Project.objects.filter(owner=request.user.id)
        serializer = ProjectSerializer(projects,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    


class ProjectGetUpdateAPIView(APIView):
    def get(self,request,pk=None):
        project = Project.objects.filter(id=pk)
        
        if not project:
            return Response(
                {'msg':"Project Not Found"},status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProjectSerializer(project)
        return Response(
            serializer.data,status=status.HTTP_200_OK
        )
        
        
    def put(self,request,pk=None,*args,**kwargs):
        project = Project.objects.get(id=pk)
        serializer = ProjectSerializer(
            project,data=request.data, partial=True
        )
        if not project:
            return Response(
                {'msg':"Project Not Found"},status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data':serializer.data},status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class DeveloperApplicationsListAPIView(APIView):
    
    def get(self,request):
        try :
            user = request.user.id
            print(user)
            
            proposals = []
            for project in Project.objects.filter(owner_id=user):
                proposals += ProjectProposal.objects.filter(
                    project=project,
                    is_apply=True
                )
            print(proposals)
            
            serializer = ProjectProposalSerializer(proposals, many=True)
            
            return Response({'applicants':serializer.data},status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response("Project Not Found",status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error':"There is an error"},status=status.HTTP_400_BAD_REQUEST)
            