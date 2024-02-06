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
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE,related_name='board')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"this {self.title} in {self.workspace.name} by {self.workspace.user}"

    
class List(models.Model):
    list_title = models.CharField(max_length=255)
    board = models.ForeignKey(Board,on_delete=models.CASCADE,related_name="lists")

    def __str__(self):
        return f"The list {self.list_title} in {self.board.title} in {self.board.workspace}"
    
    
class Card(models.Model):
    card = models.CharField(max_length=255)
    list_column = models.ForeignKey(List ,on_delete=models.CASCADE,related_name='cards')

    def __str__(self):
        return self.card