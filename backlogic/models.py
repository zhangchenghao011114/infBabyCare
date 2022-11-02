from django.db import models

# Create your models here.
class NurseInfo(models.Model):
    name = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
