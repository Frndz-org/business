from django.contrib import admin

from directory.models import Industry, Profile

# Register your models here.
admin.site.register(Industry)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
