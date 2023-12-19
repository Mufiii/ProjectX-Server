from rest_framework import serializers
from .models import *
from accounts.models import User
from developer.serializers import SkillSerializer,DevProfileListSerializer
from datetime import datetime
from django.utils import timezone

class VendorProfileChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessVendor
        fields = "__all__"
        
        
class VendorSerializer(serializers.ModelSerializer):
    vendor_profile = VendorProfileChoiceSerializer() 

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'country',
            'vendor_profile'
        ]
        
    def update(self,instance,validated_data):

        instance.first_name = validated_data.get("first_name",instance.first_name)
        instance.last_name = validated_data.get("last_name",instance.last_name)
        instance.country = validated_data.get("country",instance.country)
        
        instance.save()
        
        vendor_profile_data = validated_data.pop('vendor_profile',None)
        if vendor_profile_data:
            vendor_instance = instance.vendor_profile
            for attr,value in vendor_profile_data.items():
                setattr(vendor_instance,attr,value)
            vendor_instance.save()
            
        return instance
    
class CategoryChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class LevelChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['name']


class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())
    category = CategoryChoiceSerializer()
    level = LevelChoiceSerializer()
    # applicants = DevProfileListSerializer(many=True)
    class Meta:
        model = Project
        exclude = ('applicants',)
    
    # validate date   
    def validate_end_date(self,value):
        today = datetime.now().date()
        if value < today:
            raise serializers.ValidationError("End Date cannot be in the past.")
        return value

class ProjectProposalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectProposal
        fields = ('cover_letter','notes','approach','attachments','is_apply','developer','project')
        extra_kwargs = {
            'developer': {'required': False},
            'project': {'required': False},
        }
        
class DevSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    class Meta:
        model = Developer
        fields = ('user','skills',)
        
        
        
class ApplicationsFilterSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    applicants = DevSerializer(many=True)
    
    class Meta:
        model = Project
        fields = [
            'title',
            'skills',
            'applicants',
        ]