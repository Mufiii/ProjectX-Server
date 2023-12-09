from django.db import models
from vendor.models import BusinessVendor




class Workspace(models.Model):
    vendor = models.ForeignKey(BusinessVendor,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return f"This is the {self.name} by {self.vendor.user.first_name}"