from django.db import models
from accounts.models import User
from developer.models import Skill,Developer
# Create your models here.
  
    

class BusinessVendor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE , related_name ='vendor_profile', primary_key = True
    )
    logo = models.ImageField(upload_to='logo/', blank=True,null=True)
    banner = models.ImageField(upload_to='banner/', blank=True,null=True)
    about = models.TextField(null=True)
    description = models.TextField(null=True)
    industry = models.CharField(max_length=255)
    headquaters = models.CharField(max_length=255)
    website = models.URLField(max_length=200,blank=True)
    
    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Level(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


STATUS = [
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('completed', 'Completed')
]


class Project(models.Model):
    class PRICE_OPTIONS(models.TextChoices):
        fixed = 'Fixed-Price','Fixed-Price',
        range_ = 'Price in a range','Price in a range'
        
    owner = models.ForeignKey(BusinessVendor, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null =True,blank=True)
    note = models.TextField(null=True,blank=True)
    project_type = models.CharField(max_length=150)
    skills = models.ManyToManyField(Skill,related_name="Required_skills")
    status = models.CharField(max_length=20,choices=STATUS)
    end_date = models.DateField(blank=True,null=True)
    price_type = models.CharField(max_length=255,choices=PRICE_OPTIONS.choices)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    applicants = models.ManyToManyField(Developer, related_name='applications', through='ProjectProposal')
    
    def __str__(self) -> str:
        return self.title

                                        
   
class ProjectProposal(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    approach = models.TextField(blank=True,null=True)
    attachments = models.FileField(upload_to='pdfs/',blank=True,null=True)
    is_apply = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.developer} requested to {self.project} added by {self.project.owner}"