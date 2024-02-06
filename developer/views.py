from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import User
from vendor.models import Project, ProjectProposal
from vendor.serializer import ProjectListSerializer, ProjectProposalSerializer
# from .pagination import ProjectViewPagination
from .models import Developer, Education, Experience, Skill
from .serializers import (
    DevEducationListSerializer,
    DevEducationPostSerializer,
    DeveloperDetailSerializer,
    DevExperienceListSerializer,
    DevExperiencePostSerializer,
    SkillListUpdateSerializer,
)


class DevProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):

        user = (
            User.objects.filter(id=request.user.id)
            .select_related('dev_profile')
            .prefetch_related(
            'dev_profile__experience_set',  
            'dev_profile__education_set'  
            )
            .first()
        )
        serializer = DeveloperDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def put(self, request, *args, **kwargs):
        print("******************************")
        print(request.data,'5555555555')
        print("******************************")
        serializer = DeveloperDetailSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            user = (
                User.objects.filter(id=request.user.id)
                .select_related('dev_profile')
                .prefetch_related(
                'dev_profile__experience_set',  
                'dev_profile__education_set'  
                )
                .first()
            )
            instances = Developer.objects.filter(user=user).first()

            if "profile_picture" in request.FILES:
                instances.profile_picture = request.FILES["profile_picture"]

            if "resume" in request.FILES:
                instances.resume = request.FILES["resume"]

                instances.save()

                response_data = {
                    "msg": "Profile Updated Successfully",
                    "data": serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            user.save()

            print('+++++++++++++++++++')
            serializer.save()
            print(serializer.data)
            print('+++++++++++++++++++')
            return Response(
                {"msg": "Data Updated", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeveloperEducationListCreateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = Education.objects.filter(developer_id=request.user.id)
        serializer = DevEducationListSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DevEducationPostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                developer_instance, created = Developer.objects.get_or_create(
                    user=request.user
                )
                user = Education.objects.create(
                    developer=developer_instance,
                    school=serializer.validated_data.get("school"),
                    degree=serializer.validated_data.get("degree"),
                    field_of_study=serializer.validated_data.get("field_of_study"),
                    note=serializer.validated_data.get("note"),
                    start_date=serializer.validated_data.get("start_date"),
                    end_date=serializer.validated_data.get("end_date"),
                )
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"msg": f"There was an error: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class DeveloperEducationGetUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        instance = Education.objects.get(id=pk)
        serializer = DevEducationPostSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        instance = Education.objects.get(id=pk)
        print(instance)
        serializer = DevEducationPostSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Msg": "Data Updated", "Data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        instance = Education.objects.get(id=pk)
        instance.delete()
        return Response(
            {"Msg": "Education instance deleted sucessfully"}, status=status.HTTP_200_OK
        )


class DevExperienceListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        instance = Experience.objects.filter(developer_id=request.user.id)
        serializer = DevExperienceListSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = DevExperiencePostSerializer(data=request.data)
        developer, created = Developer.objects.get_or_create(user=request.user)
        if serializer.is_valid():
            exp = Experience.objects.create(
                developer=developer,
                designation_title=serializer.validated_data.get("designation_title"),
                company=serializer.validated_data.get("company"),
                location=serializer.validated_data.get("location"),
                country=serializer.validated_data.get("country"),
                start_date=serializer.validated_data.get("start_date"),
                end_date=serializer.validated_data.get("end_date"),
            )

            return Response(
                DevExperiencePostSerializer(exp).data, status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class DevExperienceGetUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, experience_id):
        try:
            instance = Experience.objects.get(id=experience_id)
            print(instance)
            serializer = DevExperiencePostSerializer(instance)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, experience_id):
        instance = Experience.objects.get(id=experience_id)
        print(instance)
        serializer = DevExperiencePostSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, experience_id):
        instance = Experience.objects.filter(id=experience_id)
        instance.delete()
        return Response({"Msg": "Deleted Successfully"}, status=status.HTTP_200_OK)


class DevViewProjectAPIView(APIView):
    
    def get(self, request, pk=None):
        if pk is not None:
            projects = Project.objects.filter(id=pk)
        else:
            projects = Project.objects.all()
        if not projects:
            return Response(
                {"msg": "No Projects Found"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProjectListSerializer(projects, many=True)
        # paginator = ProjectViewPagination()
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )


class DevProjectProposalView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, project_id=None):
        try:
            project = Project.objects.get(id=project_id)
            serializer = ProjectListSerializer(project)

            proposal_serializer = ProjectProposalSerializer()

            return Response(
                {"project": serializer.data, "proposal": proposal_serializer.data},
                status=status.HTTP_200_OK,
            )
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, project_id, format=None):
        project = get_object_or_404(Project, id=int(project_id))
        developer = (
            User.objects.select_related("dev_profile")
            .filter(id=request.user.id)
            .first()
        )

        serializer = ProjectProposalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            attachments_file = request.FILES.get("attachments")
            t = ProjectProposal.objects.create(
                project=project,
                developer=developer.dev_profile,
                cover_letter=serializer.validated_data.get("cover_letter"),
                notes=serializer.validated_data.get("notes"),
                approach=serializer.validated_data.get("approach"),
                attachments=attachments_file,
                is_apply=True,
            )

            return Response(
                ProjectProposalSerializer(t).data, status=status.HTTP_201_CREATED
            )

        return Response(
            {"errors": "There is an error"}, status=status.HTTP_400_BAD_REQUEST
        )


class SkillsListUpdatingAPIView(APIView):
    def get(self, request):
        q = request.GET.get("q")
        if q:
            data = Skill.objects.filter(name__istartswith=q).values()
            return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user.id
        developer = User.objects.filter(dev_profile=user).first()

        skills_data = request.data.get("skills", [])
        serializer = SkillListUpdateSerializer(data={"skills": skills_data})

        if serializer.is_valid(raise_exception=True):
            developer_profile = developer.dev_profile
            developer_profile.skills.set(skills_data)
            return Response(
                {"message": "Skills updated successfully."}, status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Invalid data provided for skills."},
            status=status.HTTP_400_BAD_REQUEST,
        )
