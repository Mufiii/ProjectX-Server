from django.db import models
from accounts.models import *
from django_countries.fields import CountryField
# Create your models here.


    
class Skill(models.Model):
    name = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
      return self.name

class DateMixin(models.Model):
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True



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
    resume = models.FileField(upload_to='resume/', null=True , blank=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    state = models.CharField(max_length=100, blank=True, null=True)
    media_links = models.URLField(max_length=200,blank=True)
    
    def __str__(self):
      return self.user.email
    
class Experience(DateMixin):
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    country = CountryField(blank_label="(select country)",null=True,blank=True)
    is_working = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class Education(DateMixin):
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE)
    school = models.CharField(max_length=255,blank=True,null=True)
    degree = models.CharField(max_length=255,blank=True,null=True)
    field_of_study = models.CharField(max_length=255,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.school} - {self.degree}"
    