from .serializer import (
    VendorSerializer,
    ProjectSerializer,
    ProjectProposalSerializer,
    ApplicationsFilterSerializer
)
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from vendor.tasks import send_email_task


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





        




class DeveloperSkillsMatchingAPIView(APIView):
    
    def get(self,request,project_id, threshold_score, format=None):
        project = Project.objects.filter(id=project_id).prefetch_related("applicants","skills")
        
        if not project:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
        )

        skills_matched = project.values('applicants__user__email','applicants__skills__name','skills__name')
        applicant_skills = {}
        skills_required = set()
            
        for entry in skills_matched:
            skills_required.add(entry['skills__name'])
            applicants = entry['applicants__user__email']
            skills = entry['applicants__skills__name']
            if applicants in applicant_skills:
                applicant_skills[applicants].append(skills)
            else:
                applicant_skills[applicants] = [skills]
                    
        matching_results = []

        for key,value in applicant_skills.items():
            data = {key:(len((set(value)).intersection(skills_required))/len(skills_required)) * 100 }
            
            if data[key] >= float(threshold_score):
                    matching_results.append(data)
                    
        # for user in matching_results:
        #     # recipient_email = user.email
        #     # print(recipient_email)
        #     subject = "Congratulations! You have been selected for Project."
        #     message = "Your custom email message goes here."
        #     print(user)
            
        #     send_email_task.delay( subject, message)
               
        return Response(
            {'data':matching_results},
            status=status.HTTP_200_OK
        )
        
 

  