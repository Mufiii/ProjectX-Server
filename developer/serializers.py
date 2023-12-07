import datetime
from rest_framework import serializers
from .models import Education,Developer,Skill,Experience
from accounts.models import User
from vendor.models import Project


class SkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Skill
        fields = ['id','name']
    
    # def update(self, instance, validated_data):
          
     

class DevProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['user','profile_picture','headline','description','gender','date_of_birth',
                  'skills','resume','city','state','media_links']
        extra_kwargs = {'user': {"read_only": True}}
               
            
class DeveloperCreateUpdateSerializer(serializers.ModelSerializer):
    dev_profile = DevProfileListSerializer()
    # Define a SerializerMethodField to handle the CountryField
    country = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "country",  
            'dev_profile'
        ]   
        
    def validate_email(self,value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email":"email already in use"})
        return value
        
    def get_country(self, obj):
        country = None

        # Check if the 'country' attribute exists
        if hasattr(obj, 'country'):
            country_object = getattr(obj, 'country')

            if country_object:
                # Modify this line to return the appropriate field or attribute from the 'Country' model
                country = country_object.name  # For example, retrieving the country's name

        return country
    
    def update(self, instance, validated_data):
        # Update User model attributes
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.country = validated_data.get('country', instance.country)

        # Update DevProfile related to the User instance
        dev_profile_data = validated_data.pop('dev_profile', None)
        if dev_profile_data:
            print(dev_profile_data["skills"])
            dev_profile_instance = instance.dev_profile  # Get the related DevProfile instance
            for attr, value in dev_profile_data.items():
                if attr != "skills":
                    setattr(dev_profile_instance, attr, value)
            skills = dev_profile_data.get('skills',{}) 
            print(skills)
            if skills: 
                dev_profile_instance.skills.clear()
                dev_profile_instance.skills.add(*skills)   
            dev_profile_instance.save()
        instance.save()
        return instance

        

class ProjectListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['id','title','description','status','note','project_type','price_type','price','category',
                  'level','skills']
        
        
        
class DevEducationListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Education
        fields = ['school','degree','field_of_study','description','start_date','end_date']   
        

class DevEducationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id','school','degree','field_of_study','description','start_date','end_date']
    
    
    def update(self, instance, validated_data):
        instance.school = validated_data.get('school',instance.school)
        instance.degree = validated_data.get('degree',instance.degree)
        instance.field_of_study = validated_data.get('field_of_study',instance.field_of_study)
        instance.description = validated_data.get('description',instance.description)
        instance.start_date = validated_data.get('start_date',instance.start_date)
        instance.end_date = validated_data.get('end_date',instance.end_date)
        instance.save()
        
        return instance 
         
        
class DevExperienceListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Experience
        fields = ['id','title','company','location','country','is_working','start_date','end_date']
        
        
class DevExperiencePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Experience
        fields = ['id','title','company','location','country','is_working','start_date','end_date']
        
        
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.company = validated_data.get('company', instance.company)
        instance.location = validated_data.get('location', instance.location)
        instance.country = validated_data.get('country', instance.country)
        instance.is_working = validated_data.get('is_working', instance.is_working)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()

        return instance