from django.contrib import admin

from .models import Board, Workspace , InviteToWorkspace

admin.site.register(Board)
@admin.register(Workspace)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id","name","description"
    )
    
admin.site.register(InviteToWorkspace) 
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id","user","workspace","token","is_accepted"
    )