from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50, null=True)
    link = models.CharField(max_length=100, null=True)
    guid = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500, null=True)
    author = models.CharField(max_length=50, null=True)
    pubdate = models.DateField(null=True)

