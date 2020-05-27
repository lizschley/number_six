from django.db import models
from autoslug import AutoSlugField


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.CharField(max_length=100)
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='title')
