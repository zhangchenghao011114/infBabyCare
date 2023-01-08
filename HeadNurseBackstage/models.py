from django.db import models

# Create your models here.
class HeadNurseInfo(models.Model):
    name = models.CharField(max_length=45,default=-1)
    username = models.CharField(max_length=45,default=-1)
    password = models.CharField(max_length=45,default=-1)
    workPermitNumber = models.CharField(max_length=45,default=-1)
    workPermitPassword = models.CharField(max_length=45,default=-1)
    login_jwt = models.CharField(max_length=500,default=-1)

class Head2Nurse(models.Model):
    nurseWorkPermitNumber = models.CharField(max_length=45,default=-1)
    headNurseWorkPermitNumber = models.CharField(max_length=45,default=-1)