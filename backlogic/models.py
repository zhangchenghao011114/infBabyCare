from django.db import models

# Create your models here.
class NurseInfo(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    workPermitNumber = models.CharField(max_length=45,default=-1)
    workPermitPassword = models.CharField(max_length=45,default=-1)