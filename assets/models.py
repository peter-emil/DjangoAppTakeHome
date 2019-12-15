from django.db import models


class MetadataEntry(models.Model):
    name = models.CharField(max_length=60, unique=True)
    string = models.TextField()


class DocumentEntry(models.Model):
    name = models.CharField(max_length=60, unique=True)
    file = models.FileField()
