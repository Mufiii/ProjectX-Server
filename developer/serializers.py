import datetime

from rest_framework import serializers

from accounts.models import User
from accounts.serializer import DeveloperChoiceSerializer

# from vendor.serializer import CategoryChoiceSerializer,LevelChoiceSerializer
from vendor.models import Project

from .models import Developer, Education, Experience, Skill


class DevEducationChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "school",
            "degree",
            "field_of_study",
            "note",
            "start_date",
            "end_date",
        ]

class DevExperienceChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "designation_title",
            "company",
            "location",
            "country",
            "is_working",
            "start_date",
            "end_date",
        ]
        
        
class SkillSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class SkillListUpdateSerializer(serializers.Serializer):
    skills = serializers.ListField(child=serializers.IntegerField())


class DevProfileListSerializer(serializers.ModelSerializer):
    user = DeveloperChoiceSerializer()

    class Meta:
        model = Developer
        fields = [
            'user',
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

    


class SkillListUpdateSerializer(serializers.Serializer):
    skills = serializers.ListField(child=serializers.IntegerField())


class DevEducationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "school",
            "degree",
            "field_of_study",
            "note",
            "start_date",
            "end_date",
        ]


class DevEducationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "school",
            "degree",
            "field_of_study",
            "note",
            "start_date",
            "end_date",
        ]

    def update(self, instance, validated_data):
        instance.school = validated_data.get("school", instance.school)
        instance.degree = validated_data.get("degree", instance.degree)
        instance.field_of_study = validated_data.get(
            "field_of_study", instance.field_of_study
        )
        instance.description = validated_data.get("description", instance.description)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.save()

        return instance
    




class DevExperienceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "company",
            "location",
            "country",
            "is_working",
            "start_date",
            "end_date",
        ]


class DevExperiencePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "designation_title",
            "company",
            "location",
            "country",
            "is_working",
            "start_date",
            "end_date",
        ]

    def update(self, instance, validated_data):
        instance.designation_title = validated_data.get("designation_title", instance.designation_title)
        instance.company = validated_data.get("company", instance.company)
        instance.location = validated_data.get("location", instance.location)
        instance.country = validated_data.get("country", instance.country)
        instance.is_working = validated_data.get("is_working", instance.is_working)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.save()

        return instance




class DeveloperProfileSerializer(serializers.ModelSerializer):
    experiences = DevExperienceChoiceSerializer(source="experience_set",many=True, read_only=True)
    educations = DevEducationChoiceSerializer(source="education_set",many=True, read_only=True)

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
            "educations",
            "experiences"
        ]

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "email already in use"})
        return value

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



class DeveloperDetailSerializer(serializers.ModelSerializer):
    dev_profile = DeveloperProfileSerializer()
    country = serializers.SerializerMethodField()
    email = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "phone",
            "country",
            "dev_profile",
        ]

    def get_country(self, obj):
        # Assuming `obj` is a User instance
        if hasattr(obj, 'dev_profile') and obj.dev_profile:
            # Check if 'country' exists in dev_profile
            country = getattr(obj.dev_profile, 'country', None)
            return str(country) if country else None
        return str(obj.country)  # Convert the Country object to its string representation


    def validate_email(self, value):
        # Profile Updation
        if not self.instance is None:
            if User.objects.exclude(id=self.instance.id).filter(email=value).exists():
                raise serializers.ValidationError(
                    {"email": "This email is already in use."}
                )
            return value
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value
    
    def update(self, instance, validated_data):
        # Update User model attributes
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.country = validated_data.get("country", instance.country)

        # Update DevProfile related to the User instance
        dev_profile_data = validated_data.pop("dev_profile", None)
        if dev_profile_data:
            print(dev_profile_data["skills"])
            dev_profile_instance = (
                instance.dev_profile
            )  # Get the related DevProfile instance
            for attr, value in dev_profile_data.items():
                if attr != "skills":
                    setattr(dev_profile_instance, attr, value)
            skills = dev_profile_data.get("skills", {})
            print(skills)
            if skills:
                dev_profile_instance.skills.clear()
                dev_profile_instance.skills.add(*skills)
            dev_profile_instance.save()
        instance.save()
        return instance