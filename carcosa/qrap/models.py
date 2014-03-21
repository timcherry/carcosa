from django.db import models

# Create your models here.
class Post(models.Model):
    company = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    comment = models.TextField()