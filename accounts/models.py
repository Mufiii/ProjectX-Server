from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField



class User(AbstractUser):
    # three user admin developer vendor
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=13, null=True,blank=True)
    country = CountryField(blank_label="(select country)",null=True,blank=True)
    
    is_developer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    

