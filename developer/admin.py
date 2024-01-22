from django.contrib import admin

from .models import Developer, Education, Experience, Skill

# Register your models here.


admin.site.register(Developer)


@admin.register(Education)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "developer",
        "school",
        "degree",
        "field_of_study",
        "note",
    )


@admin.register(Skill)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Experience)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "developer",
        "designation_title",
        "company",
        "location",
        "country",
        "is_working",
        "start_date",
        "end_date",
    )
