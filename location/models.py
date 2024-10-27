import uuid

from django.db import models

from business.models import CommonField
from directory.models import Profile as Business


# Create your models here.

class Location(CommonField):
    class STATUS(models.TextChoices):
        ACTIVE = 'ACTIVE', 'ACTIVE'
        SUSPENDED = 'SUSPENDED', 'SUSPENDED'
        DEACTIVATED = 'DEACTIVATED', 'DEACTIVATED'

    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    contact = models.CharField(max_length=25, unique=True)
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.ACTIVE)
    identifier = models.UUIDField(default=uuid.uuid4)
    business = models.ForeignKey(Business, related_name='locations', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
