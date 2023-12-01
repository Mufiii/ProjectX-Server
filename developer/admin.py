from django.contrib import admin
from .models import Developer,Skill,Education,Experience
# Register your models here.


admin.site.register(Developer)
admin.site.register(Skill)
admin.site.register(Experience)

@admin.register(Education)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','developer', 'school','degree' ,'field_of_study','description')
