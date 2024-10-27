import uuid

from django.db import models


class CommonField(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    identifier = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True
