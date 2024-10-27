from django.contrib import admin

from directory.models import Industry, Profile
from location.admin import LocationAdminInline

# Register your models here.
admin.site.register(Industry)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [LocationAdminInline]
