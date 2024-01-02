from django.shortcuts import get_object_or_404
from .serializer import (
    VendorSerializer,
    ProjectSerializer,
    ProjectProposalSerializer,
    ApplicationsFilterSerializer,
    ProjectPostSerializer,
    SkillSerializer
)
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .tasks import send_email_task
from rest_framework.parsers import JSONParser


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
          
          return Response({"data":serializer.data},status=status.HTTP_200_OK)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
              
              
          
class ProjectListCreateAPIView(APIView):
    authentication_classes=(JWTAuthentication,)
    permission_classes=(IsAuthenticated,)
    parser_classes = [JSONParser]
    
    def get(self,request):
        projects = Project.objects.filter(owner=request.user.id)
        serializer = ProjectSerializer(projects,many=True)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ProjectPostSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            skills_data = serializer.validated_data.pop("skills", [])

            # Create the project without skills first
            project = Project.objects.create(
                owner=request.user.vendor_profile,
                title=serializer.validated_data.get("title", None),
                category=serializer.validated_data.get("category", None),
                level=serializer.validated_data.get("level", None),
                description=serializer.validated_data.get("description", None),
                project_type=serializer.validated_data.get("project_type", None),
                note=serializer.validated_data.get("note", None),
                end_date=serializer.validated_data.get("end_date", None),
                price_type=serializer.validated_data.get("price_type", None),
                price=serializer.validated_data.get("price", None),
                status=serializer.validated_data.get("status", None),
            )

            # Get the skills based on the provided IDs
            skills = Skill.objects.filter(id__in=skills_data)
            required_skills = SkillSerializer(skills, many=True)

            # Set the skills for the project
            project.skills.set(skills)

            return Response(
                {'project':ProjectSerializer(project).data,'skills':required_skills.data},
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
        
 

  
class DeveloperSkillsMatchingAPIView(APIView):

    def get(self, request, project_id, threshold_score, format=None):
        project = get_object_or_404(Project, id=project_id)
        
        skills_required = set(project.skills.values_list('name', flat=True))

        matching_results = []

        for applicant in project.applicants.prefetch_related('skills').all():
            applicant_skills = set(applicant.skills.values_list('name', flat=True))
            match_percentage = len(applicant_skills.intersection(skills_required)) / len(skills_required) * 100

            if match_percentage >= float(threshold_score):
                matching_results.append({
                    'email': applicant.user.email,
                    'match_percentage': match_percentage
                })

        selected_users_emails = [result['email'] for result in matching_results]
        print(selected_users_emails)
        send_email_task.apply_async(
            kwargs={
                "selected_users_emails": selected_users_emails,
                "project_id": project_id,
            },
        )

        return Response({'data': matching_results}, status=status.HTTP_200_OK)
    
    
class ProjectSkillsGetAPIView(APIView):
    def get(self, request):
        project_id = request.GET.get('project_id') 
        project = Project.objects.get(id=project_id)
        
        ids = list(project.skills.values_list('id',flat=True))
        skills = Skill.objects.filter(id__in=ids)
        
        serialiser = SkillSerializer(
            skills,many=True
        )
        return Response(
            serialiser.data,
            status=status.HTTP_200_OK
        )