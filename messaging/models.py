from django.db import models
from tinymce.models import HTMLField


# Create your models here.

class Event(models.TextChoices):
    Nb = 'New Business', 'New Business'
    Sb = 'Suspended Business', 'New Business'
    Ab = 'Activated Business', 'Activated Business'


class Template(models.Model):
    event = models.CharField(max_length=30, unique=True, choices=Event.choices, default=Event.Nb)
    subject = models.CharField(max_length=100)
    message = HTMLField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.__str__()
