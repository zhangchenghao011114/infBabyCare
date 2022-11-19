from django.shortcuts import render, redirect, HttpResponse
from backlogic.models import NurseInfo,PatientInfo,InfusionRecords
from backlogic.jwt import generate_jwt,decode_jwt,verify_jwt
from django.views import View
import json
import os
from django.utils import timezone
import pytz
# Create your views here.
tz = pytz.timezone('Asia/Shanghai')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#前端
# class homepage(View):     
#     def get(self,request):
#         #return HttpResponse("hello")
#         print("asd\n")
#         try:
#             images = os.path.join( os.path.dirname(__file__) , 'static' )
#             img_path = os.path.join(images , 'css/bootstrap.min.css' )
#             # print(img_path)
#             file_one = open(img_path, "rb")
#         except:
#             print('fail\n')
#         return render(request,"homepage.html")



# 小程序后端
class test(View):
    def get(self,request):
        return HttpResponse("丁真测你们码")

class register(View):
    def post(self,request):
        data = json.loads(request.body)
        storejwt = data['register_jwt']
        #存储用户名密码
        register_info= decode_jwt(storejwt)
        print(register_info)
        workPermitNumber = register_info['nurse_work_permit_number']
        workPermitPassword = register_info['nurse_work_permit_password']
        username = register_info['username']
        password = register_info['password']
        name = register_info['name']
        try: 
            obj = NurseInfo.objects.filter(workPermitNumber=workPermitNumber)
            print(obj[0])
            if obj[0].workPermitNumber:
                returnjson = {'message':'already register you late pig'}
                print(returnjson)
                return HttpResponse(json.dumps(returnjson))
            else:
                returnjson = {'state':'no worknumber? you fake buster'}
                print(returnjson)
                return HttpResponse(json.dumps(returnjson))
        except IndexError:
            pass
        obj = NurseInfo.objects.create(name=name,username=username,password=password,workPermitNumber=workPermitNumber,workPermitPassword=workPermitPassword,login_jwt = storejwt)
        if obj == None :
            returnjson = {'state':'register failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'register success'}
            return HttpResponse(json.dumps(returnjson))
    def get(self,request):
            return HttpResponse("丁真测你们码")

class login(View):
    def post(self,request):
        data = json.loads(request.body)
        storejwt = data['login_jwt']
        #验证用户名密码 username, password
        disk2 = decode_jwt(storejwt)
        print(disk2)
        obj = NurseInfo.objects.filter(username=disk2['username'])
        try:
            if obj[0].password != disk2['password']:
                returndisk = {'info':'wrong password you damn ass'}
                print(returndisk)
                return HttpResponse(json.dumps(returndisk))
        except IndexError:
            returndisk = {'info':'register first you fool'}
            print(returndisk)
            return HttpResponse(json.dumps(returndisk))
        # 成功，则生成jwt,返回给客户端，并更新数据库表
        returnjwt = generate_jwt(disk2)
        obj.update(login_jwt = returnjwt)
        print(returnjwt)
        returndisk = {'jwt':returnjwt}
        return HttpResponse(json.dumps(returndisk))
    def get(self,request):
        return HttpResponse("丁真测你们码")

class infusionGroups(View):
    def get(self,request): # 获取
        # 验证http请求head中的jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse: 
            pass
        else:
            returnjson = {'state':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        
        listtext = json.loads(request.data)
        obj = PatientInfo.objects.filter(InfusionDateTime = listtext['InfusionDateTime'])
        if obj[0].InfusionDateTime: # 存在该输液记录
            returnjson = {'state':'succeess'}
            returnjson['idPatient'] = obj.idPatient
            returnjson['idNurse'] = obj.idNurse
            returnjson['idPharmaceuticals'] = obj.idPharmaceuticals
            returnjson['idPiercingTools'] = obj.idPiercingTools
            returnjson['idIntravenous'] = obj.idIntravenous
            returnjson['InfusionDateTime'] = obj.InfusionDateTime
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
        else:# 不存在该输液记录
            returnjson = {'state':'No infusion record'}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))

    def post(self,request): # 增加
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        listtext = json.loads(request.body)
        print(listtext)
        now_time = timezone.now().astimezone(tz=tz)
        now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")
        obj = InfusionRecords.objects.create(idPatient=listtext['idPatient'],idNurse=idnurse,idPharmaceuticals=listtext['idPharmaceuticals'],
        idPiercingTools=listtext['idPiercingTools'],idIntravenous=listtext['idIntravenous'],InfusionDateTime=now_time_str)
        if obj == None :
            returnjson = {'state':'add infusion record failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'add infusion record success'}
            return HttpResponse(json.dumps(returnjson))

    def put(self,request): # 修改
        return HttpResponse("change infusioninfo")

    def delete(self,request): # 删除
        return HttpResponse("delete infusioninfo")

class patientGroups(View):
    def get(self,request,patient_id): # 获取
        # 验证http请求head中的jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        #  如果病人id == listall,就返回所有该护士照顾的病人
        # 筛选
        obj = PatientInfo.objects.filter(InpatientNumber = patient_id)
        if obj[0].InpatientNumber: # 存在该病人
            returnjson = {'state':'succeess'}
            returnjson['InpatientNumber'] = obj.InpatientNumber
            returnjson['diagnosis'] = obj.diagnosis
            returnjson['bedNumber'] = obj.bedNumber
            returnjson['admissionDate'] = obj.admissionDate
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
        else:# 不存在该病人
            returnjson = {'state':'No Patient'}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))

    def post(self,request,patient_id): # 增加
        return HttpResponse("add patientinfo")

    def put(self,request,patient_id): # 修改
        return HttpResponse("change patientinfo")

    def delete(self,request,patient_id): # 删除
        return HttpResponse("delete patientinfo")

    
class img(View):
    def get(self,request,img_name):
        print(img_name)
        images = os.path.join( os.path.dirname(__file__) , 'img' )
        img_path = os.path.join(images , img_name )
        # print(img_path)
        file_one = open(img_path, "rb")
        return HttpResponse(file_one.read(), content_type='image/jpg')

class testhtml(View):
    def get(self,request,html_file):     
        print(html_file)
        css_path = os.path.join( os.path.dirname(__file__) , 'templates' )
        file_path = os.path.join(css_path , html_file )
        file_one = open(file_path, "rb")
        return HttpResponse(file_one.read(), content_type='text/html')

