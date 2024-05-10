import uuid

from django.db import models
from django_countries.fields import CountryField


# Create your models here.
class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    identifier = models.UUIDField(default=uuid.uuid4)

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name


class Profile(models.Model):
    class STATUS(models.TextChoices):
        Ac = 'ACTIVE', 'ACTIVE'
        Sup = 'SUSPENDED', 'SUSPENDED'

    name = models.CharField(max_length=300, unique=True)
    tax_id = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    industry = models.ForeignKey(Industry, related_name='businesses', on_delete=models.PROTECT)
    country = CountryField(default='GH')
    owner = models.UUIDField(default=uuid.uuid4)
    identifier = models.UUIDField(default=uuid.uuid4)
    status = models.CharField(max_length=15, choices=STATUS.choices, default=STATUS.Ac)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Stats(models.Model):
    branches = models.IntegerField(default=1)
    business = models.ForeignKey(Profile, related_name='stats', on_delete=models.CASCADE)

    def __str__(self):
        return
