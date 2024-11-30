from django.contrib import admin

from location.models import Location

# Register your models here.
admin.site.register(Location)


class LocationAdminInline(admin.StackedInline):
    model = Location
    extra = 1
