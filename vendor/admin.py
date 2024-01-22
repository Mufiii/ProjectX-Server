from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(BusinessVendor)
class adminVendor(admin.ModelAdmin):
    list_display = [
        "user",
        "logo",
        "banner",
        "about",
        "description",
        "industry",
        "headquaters",
        "website",
    ]


admin.site.register(ProjectProposal)


@admin.register(Project)
class adminProject(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(Category)
class adminCategory(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Level)
class adminLevel(admin.ModelAdmin):
    list_display = ["id", "name"]
