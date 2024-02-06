from django.contrib import admin

from .models import Board, Workspace ,Card,List

admin.site.register(Board)
admin.site.register(Card)
admin.site.register(List)

@admin.register(Workspace)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id","name","description"
    )
