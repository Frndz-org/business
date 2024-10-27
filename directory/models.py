import uuid

from django.db import models
from django_countries.fields import CountryField

from business.models import CommonField


# Create your models here.
class Industry(CommonField):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name


class Profile(CommonField):
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
    status = models.CharField(max_length=15, choices=STATUS.choices, default=STATUS.Ac)
    owner = models.UUIDField(default=uuid.uuid4)

    @property
    def industry_identifier(self):
        return self.industry.identifier.__str__()

    def __str__(self):
        return self.name


class Stats(models.Model):
    branches = models.IntegerField(default=1)
    business = models.ForeignKey(Profile, related_name='stats', on_delete=models.CASCADE)

    def __str__(self):
        return
