from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from vendor.models import Project
from .models import Invitation
from accounts.models import User
from .serializer import InvitationSerializer , HireDeveloperSerializer , DeveloperHireListSerializer
from django.conf import settings
from django.core.mail import send_mail
from threading import Thread
from developer.models import Developer



class InviteFreelancerstoProjectAPIView(APIView):
    def post(self, request):
      project_id = request.data.get('project_id')
      email = request.data.get('email')

      if project_id and email:
          try:
              project = Project.objects.get(id=project_id)

              serializer = InvitationSerializer(data={
                  'project': project.id,
                  'user': request.user.id,
                  'message': request.data.get('message'),
              })

              if serializer.is_valid(raise_exception=True):
                  serializer.save()
                  
                  subject = f"You've been invited to project {project.title}"
                  message_body = serializer.validated_data.get('message')
                  from_email = settings.EMAIL_HOST_USER
                  recipient_email = [email]
                  
                  email_thread = Thread(
                    target=send_mail, args=(subject, message_body, from_email, recipient_email)
                  )
                  email_thread.start()

                  return Response({'detail': 'Invitation sent successfully.'}, status=status.HTTP_200_OK)

          except Project.DoesNotExist:
              return Response({'detail': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)
          except User.DoesNotExist:
              return Response({'detail': 'No developer found with the provided email.'}, status=status.HTTP_404_NOT_FOUND)

      return Response({'detail': 'No project or email selected.'}, status=status.HTTP_400_BAD_REQUEST)
    


class DeveloperHiringAPIView(APIView):
    def get(self, request):
        project_id = request.GET.get('project_id')
        if project_id:
            developers = Project.objects.filter(is_hired=True, id=project_id)
            serializer = DeveloperHireListSerializer(developers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Project ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request):
        serializer = HireDeveloperSerializer(data=request.data)
        if serializer.is_valid():
            project_id = request.GET.get('project_id')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
                
                developer_id = serializer.validated_data.get('developer_id')
                try:
                    developer = Developer.objects.get(user_id=developer_id)
                except Developer.DoesNotExist:
                    return Response({'error': 'Developer not found'}, status=status.HTTP_404_NOT_FOUND)
                
                if project.applicants.filter(user_id=developer_id).exists():
                    return Response("Developer is already hired for this project", status=status.HTTP_400_BAD_REQUEST)
                else:
                    project.applicants.add(developer)
                    project.is_hired = True
                    project.save()
                    return Response({'message': 'Developer hired successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Project ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)