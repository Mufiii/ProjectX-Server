from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(BusinessVendor)
class adminVendor(admin.ModelAdmin):
    list_display = ['user', 'logo', 'banner', 'about', 'description', 'industry', 'headquaters', 'website']
    
    
admin.site.register(Level)
# admin.site.register(Project)
admin.site.register(Category)
admin.site.register(ProjectProposal)


@admin.register(Project)
class adminVendor(admin.ModelAdmin):
    list_display = ['id', 'title']
    