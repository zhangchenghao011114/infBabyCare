from django.shortcuts import render, redirect, HttpResponse
from backlogic.models import NurseInfo,PatientInfo,InfusionRecords,NurseToPaientInfo,HazardReports,InspectionReports
from backlogic.jwt import generate_jwt,decode_jwt,verify_jwt,decode_jwt_back
from django.views import View
import json
import os
from django.utils import timezone
import pytz
# Create your views here.

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
        # NurseToPaientInfo.objects.create(nurseWorkPermitNumber='114514',InpatientNumber='2020010111')
        # NurseToPaientInfo.objects.create(nurseWorkPermitNumber='114514',InpatientNumber='2020010222')
        # NurseToPaientInfo.objects.create(nurseWorkPermitNumber='114514',InpatientNumber='2020010333')
        # NurseToPaientInfo.objects.create(nurseWorkPermitNumber='114514',InpatientNumber='2020010444')
        # NurseToPaientInfo.objects.create(nurseWorkPermitNumber='114514',InpatientNumber='2020010555')
        # wrdb_nurseinfo('nurseinfo.xlsx')
        return HttpResponse("未使用的接口")

class register(View):
    def post(self,request):
        data = json.loads(request.body)
        storejwt = data['register_jwt']
        #存储用户名密码
        register_info= decode_jwt(storejwt)
        print('register.register_info:')
        print(register_info)
        workPermitNumber = register_info['nurse_work_permit_number']
        workPermitPassword = register_info['nurse_work_permit_password']
        username = register_info['username']
        password = register_info['password']
        name = register_info['name']
        try: 
            obj = NurseInfo.objects.filter(workPermitNumber=workPermitNumber)
            print('register.NurseInfo.obj[0]:')
            print(obj[0])
            if obj[0].workPermitNumber:
                returnjson = {'state':'400','message':'already register you late pig'}
                print(returnjson)
                return HttpResponse(json.dumps(returnjson))
            else:
                returnjson = {'state':'400','message':'no worknumber? you fake buster'}
                print(returnjson)
        except IndexError:
            pass
        obj = NurseInfo.objects.create(name=name,username=username,password=password,workPermitNumber=workPermitNumber,workPermitPassword=workPermitPassword,login_jwt = storejwt)
        if obj == None :
            returnjson = {'state':'400','message':'register failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
    def get(self,request):
            return HttpResponse("未使用的接口")

class login(View):
    def post(self,request):
        data = json.loads(request.body)
        storejwt = data['login_jwt']
        #验证用户名密码 username, password
        disk2 = decode_jwt(storejwt)
        print('login.前端发送过来的jwt:')
        print(disk2)
        obj = NurseInfo.objects.filter(username=disk2['username'])
        try:
            if obj[0].password != disk2['password']:
                print('login.密码错误：')
                returnjson = {'state':'400','message':'wrong password you damn ass'}
                print(returnjson)
                return HttpResponse(json.dumps(returnjson))
        except IndexError:
            returnjson = {'state':'400','message':'register first you fool'}
            print('login.未注册：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
        # 成功，则生成jwt,返回给客户端，并更新数据库表
        returnjwt = generate_jwt(disk2)
        obj.update(login_jwt = returnjwt)
        print('login.返回给小程序的jwt:')
        print(returnjwt)
        returnjwtList = []
        returnjwtList.append({'jwt':returnjwt})
        returnjson = {'state':'200','data':returnjwtList}
        return HttpResponse(json.dumps(returnjson))
    def get(self,request):
        return HttpResponse("未使用的接口")

class infusionGroups(View):
    def get(self,request): # 获取这名护士的所有输液记录
        # 验证http请求head中的jwt
        # print("infusionGroups.get")
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse: 
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        
        # 根据护士id查找输液记录
        obj = InfusionRecords.objects.filter(idNurse = idnurse)
        InfusionRecordList = []
        for item in obj:
            if item.infusionDateTime: # 存在该输液记录
                recordjson = {}
                recordjson['idPatient'] = item.idPatient
                recordjson['idPharmaceuticals'] = item.idPharmaceuticals
                recordjson['idPiercingTools'] = item.idPiercingTools
                recordjson['idIntravenous'] = item.idIntravenous
                recordjson['infusionDateTime'] = item.infusionDateTime
                InfusionRecordList.append(recordjson)
        print('infusionGroups.get.这名护士的所有输液记录:')
        print(InfusionRecordList)
        returnjson = {'state':'200','data':InfusionRecordList}
        return HttpResponse(json.dumps(returnjson))

    def post(self,request): # 增加
        print("infusionGroups.post")
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        listtext = json.loads(request.body)
        print('小程序发送过来的信息 request.body:')
        print(listtext)
        tz = pytz.timezone('Asia/Shanghai')
        now_time = timezone.now().astimezone(tz=tz)
        now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")
        obj = InfusionRecords.objects.create(idPatient=listtext['idPatient'],idNurse=idnurse,idPharmaceuticals=listtext['idPharmaceuticals'],
        idPiercingTools=listtext['idPiercingTools'],idIntravenous=listtext['idIntravenous'],infusionDateTime=now_time_str)
        if obj == None :
            returnjson = {'state':'400','message':'add infusion record failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))

    def put(self,request): # 修改
        print('infusionGroups.put 修改')
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据传递过来的内容修改输液记录
        listtext = json.loads(request.body)
        print(listtext)
        infusion_obj = InfusionRecords.objects.filter(infusionDateTime = listtext['infusionDateTime']).first()
        if infusion_obj.idNurse == idnurse:
                # if listtext['idPiercingTools']:
                infusion_obj.idPiercingTools = listtext['idPiercingTools']
                # if listtext['idIntravenous']:
                infusion_obj.idIntravenous = listtext['idIntravenous']
                # if listtext['idPharmaceuticals']:
                infusion_obj.idPharmaceuticals = listtext['idPharmaceuticals']
                infusion_obj.save()
                print('infusionGroups.put 成功修改')
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        else:
            returnjson = {'state':'400','message':'在此时间，没有该护士提交的输液记录'}
            return HttpResponse(json.dumps(returnjson))
       
    def delete(self,request): # 删除
        print("infusionGroups.delete")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据传递过来的内容修改输液记录
        obj = InfusionRecords.objects.filter(idNurse = idnurse)
        listtext = json.loads(request.body)
        for item in obj:
            if item.infusionDateTime == listtext['infusionDateTime']: # 存在该输液记录
                item.delete() 
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        returnjson = {'state':'400','message':'这个输液记录不存在啊'}
        return HttpResponse(json.dumps(returnjson))

class hazardGroups(View):
    def get(self,request): # 获取这名护士隐患报告
        print("hazardGroups.get")
        # 验证http请求head中的jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse: 
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        
        # 根据护士id查找隐患报告
        obj = HazardReports.objects.filter(idNurse = idnurse)
        HazardReportList = []
        for item in obj:
            if item.hazardDateTime: # 存在该隐患报告
                recordjson = {}
                recordjson['location'] = item.location
                recordjson['hazardInfo'] = item.hazardInfo
                recordjson['hazardDateTime'] = item.hazardDateTime
                HazardReportList.append(recordjson)
        print('这名护士的所有隐患报告:')
        print(HazardReportList)
        returnjson = {'state':'200','data':HazardReportList}
        return HttpResponse(json.dumps(returnjson))

    def post(self,request): # 增加
        print("hazardGroups.post")
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))

        listtext = json.loads(request.body)
        print('hazardGroups.get.小程序发送过来的信息:')
        print(listtext)
        tz = pytz.timezone('Asia/Shanghai')
        now_time = timezone.now().astimezone(tz=tz)
        now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")
        obj = HazardReports.objects.create(idNurse = idnurse, location = listtext['location'], 
        hazardInfo = listtext['hazardInfo'], hazardDateTime = now_time_str )
        if obj == None :
            returnjson = {'state':'400','message':'add hazard report failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))

    def put(self,request): # 修改
        print("hazardGroups.put")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据传递过来的内容修改隐患报告
        listtext = json.loads(request.body)
        #TODO 在这里添加报告修改时间限制，报告提交24小时后护士失去修改权限
        print(listtext)
        hazard_obj = HazardReports.objects.filter(hazardDateTime = listtext['hazardDateTime']).first()
        if hazard_obj.idNurse == idnurse:
                # if listtext['location']:
                hazard_obj.location = listtext['location']
                # if listtext['hazardInfo']:
                hazard_obj.hazardInfo = listtext['hazardInfo']
                hazard_obj.save()
                print('hazardGroups.put 成功修改')
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        else:
            returnjson = {'state':'400','message':'在此时间，有该护士提交的隐患报告'}
            return HttpResponse(json.dumps(returnjson))

    def delete(self,request): # 删除
        print("hazardGroups.delete")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据传递过来的内容删除隐患报告
        obj = HazadrReports.objects.filter(idNurse = idnurse)
        listtext = json.loads(request.body)
        #TODO 在这里添加报告删除时间限制，报告提交24小时后护士失去删除权限
        for item in obj:
            if item.hazardDateTime == listtext['hazardDateTime']: # 存在该隐患报告
                item.delete() 
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        returnjson = {'state':'400','message':'在此时间，没有该护士提交的隐患报告'}
        return HttpResponse(json.dumps(returnjson))

class inspectionGroups(View):
    def get(self,request): # 获取这名护士巡视报告
        print("inspectionGroups get")
        # 验证http请求head中的jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse: 
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        
        # 根据护士id查找巡视报告
        obj = InspectionReports.objects.filter(idNurse = idnurse)
        InspectionReportList = []
        for item in obj:
            if item.inspectionDateTime: # 存在该巡视报告
                recordjson = {}
                recordjson['location'] = item.location
                recordjson['inspectionInfo'] = item.inspectionInfo
                recordjson['inspectionDateTime'] = item.inspectionDateTime
                InspectionReportList.append(recordjson)
        
        print(InspectionReportList)
        returnjson = {'state':'200','data':InspectionReportList}
        return HttpResponse(json.dumps(returnjson))

    def post(self,request): # 增加
        print("inspectionGroups post")
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))

        listtext = json.loads(request.body)
        print(listtext)
        tz = pytz.timezone('Asia/Shanghai')
        now_time = timezone.now().astimezone(tz=tz)
        now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")
        obj = InspectionReports.objects.create(idNurse=idnurse,location=listtext['location'],
        inspectionInfo=listtext['inspectionInfo'],inspectionDateTime=now_time_str)
        if obj == None :
            returnjson = {'state':'400','message':'add inspection report failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))

    def put(self,request): # 修改
        print("inspectionGroups put")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据传递过来的内容修改巡视报告
        listtext = json.loads(request.body)
        #TODO 在这里添加报告修改时间限制，报告提交24小时后护士失去修改权限
        print(listtext)
        inspection_obj = InspectionReports.objects.filter(inspectionDateTime = listtext['inspectionDateTime']).first()
        if inspection_obj.idNurse == idnurse:
                # if listtext['location']:
                inspection_obj.location = listtext['location']
                # if listtext['inspectionInfo']:
                inspection_obj.inspectionInfo = listtext['inspectionInfo']
                inspection_obj.save()
                print('hazardGroups.put 成功修改')
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        else:
            returnjson = {'state':'400','message':'在此时间，没有该护士提交的巡视报告'}
            return HttpResponse(json.dumps(returnjson))

    def delete(self,request): # 删除
        print("inspectionGroups delete")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据传递过来的内容删除隐患报告
        obj = InspectionReports.objects.filter(idNurse = idnurse)
        listtext = json.loads(request.body)
        #TODO 在这里添加报告删除时间限制，报告提交24小时后护士失去删除权限
        for item in obj:
            if item.inspectionDateTime == listtext['inspectionDateTime']: # 存在该隐患报告
                item.delete() 
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        returnjson = {'state':'400','message':'在此时间，没有该护士提交的隐患报告'}
        return HttpResponse(json.dumps(returnjson))

class patientGroups(View):
    def get(self,request,patient_id): # 获取
        print("patientGroups.get")
        # 验证http请求head中的jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        #  如果病人id == listall,就返回所有该护士照顾的病人
        if patient_id == 'listall':
            obj = NurseToPaientInfo.objects.filter(nurseWorkPermitNumber = idnurse)
        else:
            # 筛选
            obj = PatientInfo.objects.filter(InpatientNumber = patient_id)
            PatientInfoList = []
            if obj[0].InpatientNumber: # 存在该病人
                recordjson = {}
                recordjson['name'] = obj[0].name
                recordjson['diagnosis'] = obj[0].diagnosis
                recordjson['bedNumber'] = obj[0].bedNumber
                recordjson['admissionDate'] = obj[0].admissionDate
                recordjson['img_url'] = 'http://ibf.whiteffire.cn:8001/img/patient_' + obj[0].InpatientNumber + '.jpg'   
                print('img_url:')
                print(recordjson['img_url']) 
                PatientInfoList.append(recordjson)
                returnjson = {'state':'200','data':PatientInfoList}
                return HttpResponse(json.dumps(returnjson))
            else:# 不存在该病人
                returnjson = {'state':'400','message':'No Patient'}
                print(returnjson)
                return HttpResponse(json.dumps(returnjson))

    def post(self,request,patient_id): # 增加
        print("patientGroups.post")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        #验证病人是否已存在
        listtext = json.loads(request.body)
        print(listtext)

        # files = request.FILES
        # content = files.get('image',None).read();        
        # name = listtext['name'] = '.jpg'
        # path = os.path.join(settings.IMAGES_DIR,name) 
        # with open(path,'wb') as f:
        #     f.write(content)   
            
        try:
            patient_obj = PatientInfo.objects.filter(InpatientNumber = patient_id)
            if patient_obj[0]:
                returnjson = {'state':'400','message':'patient is already exist'}
                print(returnjson)
                return HttpResponse(json.dumps(returnjson))
        except IndexError:
            pass
        #获取图片
        # image_name = 'image'
        # image = request.FILES.get(image_name)

        # images = os.path.join( os.path.dirname(__file__) , 'img' )
        # img_path = os.path.join(images , image_name )

        # # 将图片保存到本地
        # with open(img_path, 'wb') as f:
        #     for chunk in image.chunks():
        #         f.write(chunk)

        obj = PatientInfo.objects.create(name=listtext['name'],InpatientNumber=patient_id,diagnosis=listtext['diagnosis'],bedNumber=listtext['bedNumber'],admissionDate=listtext['admissionDate'])
        NurseToPaientInfo.objects.create(nurseWorkPermitNumber = idnurse,InpatientNumber = patient_id)
        if obj == None :
            returnjson = {'state':'400','message':'add patient failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))

    def put(self,request,patient_id): # 修改
        print("patientGroups.put")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据护士id,找出ta照顾的所有病人
        try:
            obj = NurseToPaientInfo.objects.filter(nurseWorkPermitNumber = idnurse)
            if obj[0].nurseWorkPermitNumber:
                pass
        except IndexError:
            print('patientGroups put 错误发生在 patient2nurse line_17\n')
            returnjson = {'state':'400','message':'The nurse did not take care of any patients'}
        paitentIdList = []
        for item in obj:
            paitentIdList.append(item.InpatientNumber)
        # 根据传递过来的内容修改病人信息
         #TODO 可修改病人id
        listtext = json.loads(request.body)
        
        for item in paitentIdList:
            if item == patient_id: # 存在该病人信息
                patient_obj = PatientInfo.objects.filter(InpatientNumber = item).first()
                # if listtext['name']:
                patient_obj.name = listtext['name']
                # if listtext['diagnosis']:
                patient_obj.diagnosis = listtext['diagnosis']
                # if listtext['bedNumber']:
                patient_obj.bedNumber = listtext['bedNumber']
                # if listtext['admissionDate']:
                patient_obj.admissionDate = listtext['admissionDate'] 
                # if listtext['imgPath']:
                #     patient_obj.photoAddress = listext['imgPath']
                patient_obj.save()
                #     files = request.FILES
                # if files.get('image'):
                #     content = files.get('image',None).read();        
                #     name = patient_obj[0].name + '.jpg'
                #     path = os.path.join(settings.IMAGES_DIR,name) 
                #     with open(path,'wb') as f:
                #         f.write(content)   
                                
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        returnjson = {'state':'400','message':'No InpatientNumber matches among the patients you manage'}
        return HttpResponse(json.dumps(returnjson))

    def delete(self,request,patient_id): # 删除
        print("patientGroups.delete")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 根据护士id,找出ta照顾的所有病人
        try:
            obj = NurseToPaientInfo.objects.filter(nurseWorkPermitNumber = idnurse)
            if obj[0].nurseWorkPermitNumber:
                pass
        except IndexError:
            print('patientGroups delete 错误发生在 patient2nurse line_17\n')
            returnjson = {'state':'400','message':'The nurse did not take care of any patients'}
        paitentIdList = []
        for item in obj:
            paitentIdList.append(item.InpatientNumber)
        # 根据传递过来的内容删除隐患报告
        for item in paitentIdList:
            if item == patient_id: # 存在该病人信息
                patient_obj = PatientInfo.objects.filter(InpatientNumber = item)
                patient_obj[0].delete()
                NurseToPaientInfo.objects.filter(nurseWorkPermitNumber = idnurse,InpatientNumber = item).delete() 
                InfusionRecords.objects.filter(idPatient = patient_id).delete() 
                return HttpResponse(json.dumps({'state':'200','data':[]}))
        returnjson = {'state':'400','message':'No InpatientNumber matches among the patients you manage'}
        return HttpResponse(json.dumps(returnjson))

class nurseGroups(View):
    def get(self,request): # 获取
        print("nurseGroups.get:")
        # 验证http请求head中的jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        # 返回护士个人信息
        obj = NurseInfo.objects.filter(workPermitNumber = idnurse)
        NurseInfoList = []
        if obj[0].workPermitNumber: 
            recordjson = {}
            recordjson['name'] = obj[0].name
            recordjson['workPermitNumber'] = obj[0].workPermitNumber
            recordjson['img_url'] = 'http://ibf.whiteffire.cn:8001/img/nurse_' + obj[0].workPermitNumber + '.jpg'  
            NurseInfoList.append(recordjson)
            returnjson = {'state':'200','data':NurseInfoList}
            return HttpResponse(json.dumps(returnjson))
        else:# 不存在该输液记录
            returnjson = {'state':'400','message':'No infusion record'}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))

class patient2nurse(View):
    def get(self,request):# get all patients of this nurse
        print("patient2nurse.get")
        # 验证http请求head中的jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))
        
        # # 获取该名护士照顾的所有病人的信息
        # # 验证http请求head中的jwt
        # verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        # print('patient2nurse:')
        # print(verification_jwt)

        # # 建议传过来的jwt是否可解码
        # payload = decode_jwt_back(verification_jwt)
        # if payload:
        #     pass
        # else:
        #     returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
        #     return HttpResponse(json.dumps(returnjson))

        # # 可解码的情况下，判断该jwt是否与数据库中的jwt相同，不同则说明这个jwt是被顶掉的
        # idnurse = verify_jwt(verification_jwt)
        # print(idnurse)
        # if idnurse:
        #     pass
        # else:
        #     returnjson = {'state':'400','message':'您的账户在异地登录'}
        #     return HttpResponse(json.dumps(returnjson))
        # 根据护士id,找出ta照顾的所有病人
        try:
            obj = NurseToPaientInfo.objects.filter(nurseWorkPermitNumber = idnurse)
            if obj[0].nurseWorkPermitNumber:
                # print(obj[0].id)
                pass
        except IndexError:
            print('patient2nurse get 错误发生在 patient2nurse line_17\n')
            returnjson = {'state':'400','message':'该护士没有照顾任何病人'}
        paitentIdList = []
        for item in obj:
            paitentIdList.append(item.InpatientNumber)
        paitentInfoList = []
        print(paitentIdList)
        for item in paitentIdList:
            try:
                tempObj = PatientInfo.objects.filter(InpatientNumber = item)
                if tempObj[0].InpatientNumber: 
                    recordjson = {}
                    recordjson['InpatientNumber'] = tempObj[0].InpatientNumber
                    recordjson['name'] = tempObj[0].name
                    recordjson['diagnosis'] = tempObj[0].diagnosis
                    recordjson['bedNumber'] = tempObj[0].bedNumber
                    recordjson['admissionDate'] = tempObj[0].admissionDate
                    recordjson['img_url'] = 'http://ibf.whiteffire.cn:8001/img/patient_' + tempObj[0].InpatientNumber + '.jpg'   
                    printMsg = 'img_url:' + recordjson['img_url']
                    print(printMsg)       
                    paitentInfoList.append(recordjson)
            except IndexError:
                print('错误发生在 patient2nurse line_35\n')
        returnjson = {'state':'200','data':paitentInfoList}
        return HttpResponse(json.dumps(returnjson))

class img(View):
    def get(self,request,img_name):
        printMsg = "img.get:" + img_name
        print(printMsg)
        images = os.path.join( os.path.dirname(__file__) , 'img' )
        img_path = os.path.join(images , img_name )
        # print(img_path)
        file_one = open(img_path, "rb")
        return HttpResponse(file_one.read(), content_type='image/jpg')
# # 导入 Django 模块
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.db import models

# # 定义图片上传模型
# class Image(models.Model):
#     path = models.CharField(max_length=256)

# 定义图片上传视图函数
class upload_patient_image(View):
    def post(self,request,patient_id):
        print("upload_patient_image post")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))

        # 根据护士id,找出ta照顾的所有病人
        try:
            obj = NurseToPaientInfo.objects.filter(nurseWorkPermitNumber = idnurse)
            if obj[0].nurseWorkPermitNumber:
                pass
        except IndexError:
            print('upload_patient_image post 错误发生在该护士没有照顾病人 \n')
            returnjson = {'state':'400','message':'The nurse did not take care of any patients'}
            return HttpResponse(json.dumps(returnjson))

        paitentIdList = []
        for item in obj:
            paitentIdList.append(item.InpatientNumber)
        # 获取上传的图片文件
        files = request.FILES
        if files.get('image',None):
            pass
        else:
            returnjson = {'state':'400','message':'no images'}
            return HttpResponse(json.dumps(returnjson))

        # 将图片路径存入数据库
        # image = Image(path = img_path)
        # image.save()
        for item in paitentIdList:
            if item == patient_id: # 存在该病人信息
                patient_obj = PatientInfo.objects.filter(InpatientNumber = item).first()
                images_dir = os.path.join( os.path.dirname(__file__) , 'img' )
                image_name = 'patient_' + patient_obj.InpatientNumber + '.jpg'
                img_path = os.path.join(images_dir , image_name )
                print('img_path')
                print(img_path)
                # if img_path:
                #     patient_obj.photoAddress = img_path
                # patient_obj.save()
                image = files.get('image',None)
                print('image')
                print(image)
                # 将图片保存到本地
                with open(img_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                returnjson = {'state':'200','data':[]}
                return HttpResponse(json.dumps(returnjson))
        returnjson = {'state':'400','message':'Image No InpatientNumber matches among the patients you manage'}
        return HttpResponse(json.dumps(returnjson))
    # return render(request, 'upload_image.html')

class upload_nurse_image(View):
    def post(self,request):
        print("upload_nurse_image post")
        #验证jwt
        verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idnurse = verify_jwt(verification_jwt)
        if idnurse:
            pass
        else:
            returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
            return HttpResponse(json.dumps(returnjson))

        # 获取上传的图片文件
        files = request.FILES
        if files.get('image',None):
            pass
        else:
            returnjson = {'state':'400','message':'no images'}
            return HttpResponse(json.dumps(returnjson))

        # 将图片路径存入数据库
        nurse_obj = NurseInfo.objects.filter(workPermitNumber = idnurse).first()
        images_dir = os.path.join( os.path.dirname(__file__) , 'img' )
        image_name = 'nurse_' + nurse_obj.workPermitNumber + '.jpg'
        img_path = os.path.join(images_dir , image_name )
        # if img_path:
        #     nurse_obj.photoAddress = img_path
        # nurse_obj.save()
        image = files.get('image',None)
        print('image')
        print(image)
        # 将图片保存到本地
        with open(img_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        returnjson = {'state':'200','data':[]}
        return HttpResponse(json.dumps(returnjson))
        # returnjson = {'state':'400','message':'Image No InpatientNumber matches among the patients you manage'}
        # return HttpResponse(json.dumps(returnjson))
    # return render(request, 'upload_image.html')

class testhtml(View):
    def get(self,request,html_file):     
        print(html_file)
        css_path = os.path.join( os.path.dirname(__file__) , 'templates' )
        file_path = os.path.join(css_path , html_file )
        file_one = open(file_path, "rb")

        return HttpResponse(file_one.read(), content_type='text/html')

