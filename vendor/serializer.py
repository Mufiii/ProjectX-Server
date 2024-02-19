from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from accounts.models import User
from developer.serializers import DevProfileListSerializer, SkillSerializer
from .models import *


class VendorProfileChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessVendor
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    vendor_profile = VendorProfileChoiceSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "country", "vendor_profile"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.country = validated_data.get("country", instance.country)

        instance.save()

        vendor_profile_data = validated_data.pop("vendor_profile", None)
        if vendor_profile_data:
            vendor_instance = instance.vendor_profile
            for attr, value in vendor_profile_data.items():
                setattr(vendor_instance, attr, value)
            vendor_instance.save()

        return instance


class CategoryChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class LevelChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["name"]


class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())
    category = CategoryChoiceSerializer()
    level = LevelChoiceSerializer()
    applicants = DevProfileListSerializer(many=True)
    
    class Meta:
        model = Project
        fields = "__all__"


class ProjectPostSerializer(serializers.ModelSerializer):
    skills = serializers.ListField()

    class Meta:
        model = Project
        fields = [
            "category",
            "level",
            "title",
            "description",
            "note",
            "project_type",
            "skills",
            "status",
            "end_date",
            "price_type",
            "price",
        ]

    # validate date
    def validate_end_date(self, value):
        today = datetime.now().date()
        if value < today:
            raise serializers.ValidationError("End Date cannot be in the past.")
        return value

    # def create(self, validated_data):
    #     skills_data = validated_data.pop("skills", [])
    #     project = super().create(validated_data)  # Call the create method of the base class

    #     # Add the skills to the project
    #     project.skills.set(skills_data)
    #     return project


class ProjectProposalSerializer(serializers.ModelSerializer):
    # developer = DevProfileListSerializer(required=False)
    # project = ProjectSerializer(required=False)
    class Meta:
        model = ProjectProposal
        fields = ("cover_letter", "notes", "approach", "attachments", "is_apply")
        
        
class ProjectProposalChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectProposal
        fields = ("cover_letter", "notes", "approach", "attachments")

class ProjectProposalGetSerializer(serializers.ModelSerializer):
    developer = DevProfileListSerializer()
    project = ProjectSerializer()
    class Meta:
        model = ProjectProposal
        fields = ('developer','project',"cover_letter", "notes", "approach", "attachments", "is_apply")


class DevSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Developer
        fields = (
            "user",
            "skills",
        )


class ApplicationsFilterSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    applicants = DevSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "title",
            "skills",
            "applicants",
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    category = CategoryChoiceSerializer()
    level = LevelChoiceSerializer()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "status",
            "note",
            "project_type",
            "price_type",
            "price",
            "category",
            "level",
            "skills",
            "created_at",
            "updated_at",
        ]


class DevProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = [
            "profile_picture",
            "headline",
            "description",
            "gender",
            "date_of_birth",
            "skills",
            "resume",
            "city",
            "state",
            "media_links",
        ]
        extra_kwargs = {"user": {"read_only": True}}



class DeveloperListSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    dev_profile = DevProfileSerializer()
    class Meta:
        model = User
        fields = ["id", "first_name", "username", "last_name", "email", "country",'dev_profile']
    
    def get_country(self, obj):
        country = None

        # Check if the 'country' attribute exists
        if hasattr(obj, "country"):
            country_object = getattr(obj, "country")

            if country_object:
                # Modify this line to return the appropriate field or attribute from the 'Country' model
                country = (
                    country_object.name
                )  # For example, retrieving the country's name

        return country
    
    
class ApplicantSerializer(serializers.Serializer):
    proposal = ProjectProposalChoiceSerializer()
    
    class Meta:
        model = ProjectProposal
        fields = ('proposal',)
    