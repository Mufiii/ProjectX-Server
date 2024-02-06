from django.db import models
from vendor.models import Project
from accounts.models import User



class Invitation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    message = models.TextField()
    is_invited = models.BooleanField(default=False)
    
    