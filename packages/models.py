from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100, null=True)
    author_email = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=300, null=True)
    keywords = models.CharField(max_length=200, null=True)
    version = models.CharField(max_length=10, null=True)
    maintainer = models.CharField(max_length=100, null=True)
    maintainer_email = models.CharField(max_length=100, null=True)