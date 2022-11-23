from django.db import models

# 护士长表
class HeadNurseInfo(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    workPermitNumber = models.CharField(max_length=45,default=-1)
    workPermitPassword = models.CharField(max_length=45,default=-1)
    login_jwt = models.CharField(max_length=200,default=-1)
 
# 护士表
class NurseInfo(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    workPermitNumber = models.CharField(max_length=45,default=-1)
    workPermitPassword = models.CharField(max_length=45,default=-1)
    login_jwt = models.CharField(max_length=500,default=-1)


# 病人表
class PatientInfo(models.Model):
    name = models.CharField(max_length=45)
    InpatientNumber = models.CharField(max_length=45,default=-1)
    diagnosis = models.CharField(max_length=45,default=-1)
    bedNumber = models.CharField(max_length=45,default=-1)
    admissionDate = models.CharField(max_length=45,default=-1)

#护士管哪些病人,病人和护士是多对多的关系
class NurseToPaientInfo(models.Model):
    nurseWorkPermitNumber = models.CharField(max_length=45,default=-1)
    InpatientNumber = models.CharField(max_length=45,default=-1)

# 隐患报告表
class HazardReports(models.Model):
    idNurse = models.CharField(max_length=45,default=-1)         #提交报告的护士
    location = models.CharField(max_length=45,default=-1)        #地点
    hazardInfo = models.CharField(max_length=45,default=-1)      #隐患报告信息
    hazardDateTime = models.CharField(max_length=45,default=-1)  #报告时间

# 巡视报告表
class InspectionReports(models.Model):
    idNurse = models.CharField(max_length=45,default=-1)             #提交报告的护士
    location = models.CharField(max_length=45,default=-1)            #地点
    inspectionInfo = models.CharField(max_length=45,default=-1)      #巡视报告信息
    inspectionDateTime = models.CharField(max_length=45,default=-1)  #报告时间

# 输液记录表
class InfusionRecords(models.Model):
    idPatient = models.CharField(max_length=45)
    idNurse = models.CharField(max_length=45,default=-1)
    idPharmaceuticals = models.CharField(max_length=45,default=-1)  #药品id
    idPiercingTools = models.CharField(max_length=45,default=-1)    #穿刺工具id
    idIntravenous = models.CharField(max_length=45,default=-1)      #静脉id
    infusionDateTime = models.CharField(max_length=45,default=-1)   #注射时间

# 静脉表
class IntravenousInfo(models.Model):
    IntravenousName = models.CharField(max_length=45)
    IntravenousDiameter = models.CharField(max_length=45,default=-1)

# 药物表
class PharmaceuticalsInfo(models.Model):
    PharmaceuticalsType = models.CharField(max_length=45)
    PharmaceuticalsQR = models.CharField(max_length=45,default=-1)

# 穿刺工具表
class PiercingToolsInfo(models.Model):
    PiercingToolsName = models.CharField(max_length=45)
    PiercingToolsRetentionTime = models.CharField(max_length=45,default=-1)
    PiercingApplicationScope = models.CharField(max_length=45,default=-1)
