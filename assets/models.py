from django.db import models
from django.contrib.auth.models import User


class MetadataEntry(models.Model):
    name = models.CharField(max_length=60, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    string = models.TextField()


class DocumentEntry(models.Model):
    name = models.CharField(max_length=60, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.URLField()
