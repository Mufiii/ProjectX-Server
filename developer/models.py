from django.db import models
from accounts.models import *
# Create your models here.


    
class Skill(models.Model):
    name = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
      return self.name


GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]

class Developer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE , related_name ='dev_profile', primary_key = True
    )
    profile_picture = models.ImageField(upload_to="profile/developer/",blank=True,null=True)
    headline = models.CharField(max_length=255,null=True)
    description = models.TextField(blank=True,null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES) 
    date_of_birth = models.DateField(null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    experience = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resume/', null=True , blank=True)
    qualification = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    media_links = models.URLField(max_length=200,blank=True)
    
    def __str__(self):
      return self.user.email
    

    