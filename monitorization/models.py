from django.db import models
from accounts.models import User
from vendor.models import BusinessVendor


class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="workspace")
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length = 255,blank=True,null=True, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"This is the {self.name} by {self.user.first_name}"


class Board(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"this {self.title} in {self.workspace.name} by {self.workspace.user}"



class Card(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
 

class InviteToWorkspace(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    workspace = models.ForeignKey('Workspace', on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    is_accepted = models.BooleanField(default=False)
    
    def __str__(self) :
        return f"invite link from {self.workspace} by {self.user}"