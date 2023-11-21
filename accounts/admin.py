from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import Group

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'username','first_name' ,'last_name','country','is_active','is_developer','is_vendor')

