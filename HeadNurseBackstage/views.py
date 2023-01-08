from django.shortcuts import render, redirect, HttpResponse
from django.http import QueryDict
from HeadNurseBackstage.models import HeadNurseInfo, Head2Nurse
from backlogic.models import NurseInfo,InspectionReports,HazardReports,NurseToPaientInfo
from backlogic.jwt import generate_jwt,decode_jwt,verify_jwt,decode_jwt_back
from django.views import View
import json
import os
from django.utils import timezone
import pytz
import time
from urllib import parse

def logpage(request):
    if request.method == "GET":
        return render(request,"logpage.html")
    elif request.method == "POST":
        data = json.loads(request.body)
        storejwt = data['login_jwt']
        #验证用户名密码 username, password
        disk2 = decode_jwt(storejwt)
        print('login.前端发送过来的jwt:')
        returnjwt = generate_jwt(disk2)
        print(disk2)
        obj = HeadNurseInfo.objects.filter(username=disk2['username'])
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
        print('login.返回给管理端的jwt:')
        obj.update(login_jwt = returnjwt)
        print(returnjwt)
        returnjwtList = []
        returnjwtList.append({'jwt':returnjwt})
        returnjson = {'state':'200','data':returnjwtList}
        return HttpResponse(json.dumps(returnjson))
        
def registerpage(request):
    if request.method == "GET":
        return render(request,"registerpage.html")
    elif request.method == "POST":
        data = json.loads(request.body)
        print(data)
        storejwt = data['register_jwt']
        #存储用户名密码
        register_info= decode_jwt(storejwt)
        print(register_info)
        workPermitNumber = register_info['NurseWorkPermitNumber']
        workPermitPassword = register_info['NurseWorkPermitPassword']
        username = register_info['username']
        password = register_info['password']
        name = register_info['NurseName']
        
        try: 
            obj = HeadNurseInfo.objects.filter(workPermitNumber=workPermitNumber)
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
        obj = HeadNurseInfo.objects.create(name=name,username=username,password=password,workPermitNumber=workPermitNumber,workPermitPassword=workPermitPassword,login_jwt = storejwt)
        if obj == None :
            returnjson = {'state':'400','message':'register failed'}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
    
def mainpage(request):
    if request.method == "GET":
        try:
            # get all the parameters
            username = request.get_full_path().split("?")[1].split('&')[0].split("=")[1]
            jwt = request.get_full_path().split("?")[1].split('&')[1].split("=")[1]
            print("mainpage.receive jwt: ",jwt)
            print("receive username: ",username)
            if username == "" or jwt == "" or jwt == "0":
                return redirect("/")  
        except:
            return redirect("/")       
        timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return render(request,"mainpage.html",{"username":username,"time":timenow})

def nursemanagementpage(request):
    if request.method == "GET":
        try:
            username = request.get_full_path().split("?")[1].split('&')[0].split("=")[1]
            jwt = request.get_full_path().split("?")[1].split('&')[1].split("=")[1]
            print("nursepage.receive jwt: ",jwt)
            print("nursemanage.receive username: ",username)
            if username == "" or jwt == "" or jwt == "0":
                return redirect("/")  
        except:
            return redirect("/")
        nursedata = {}
        idhead = HeadNurseInfo.objects.filter(login_jwt=jwt)[0].workPermitNumber
        try:
            objs = Head2Nurse.objects.filter(headNurseWorkPermitNumber=idhead)
            if objs[0].nurseWorkPermitNumber:
                print(objs[0].nurseWorkPermitNumber)
                pass
        except IndexError:
            print('nursemanagement.get')
            returnjson = {'state':'400','message':'该护士长没有任何护士'}
        for obj in objs:
            print(obj.nurseWorkPermitNumber)
            obj = NurseInfo.objects.filter(workPermitNumber=obj.nurseWorkPermitNumber)[0]
            nursedata[str(obj.id)] = {
                "NurseName":obj.name,
                "NurseworkPermitNumber": obj.workPermitNumber,
                "NurseworkPermitPassword":obj.workPermitPassword,
                "username":obj.username,
                "password":obj.password
            }
        timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return render(request,"nursemanagementpage.html",{"nursedata":nursedata,"username":username,"time":timenow})
    elif request.method == "POST":
        print(request.method)
        listtext = json.loads(request.body)
        print(listtext)
        loginjwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        print(loginjwt)
        idhead = HeadNurseInfo.objects.filter(login_jwt=loginjwt)[0].workPermitNumber
        try:
            idhead = HeadNurseInfo.objects.filter(login_jwt=loginjwt)[0].workPermitNumber
        except IndexError:
            print('nursemanagement.POST')
            returnjson = {'state':'400','message':'哪来的这个护士长，不存在啊'}
        nurse = NurseInfo.objects.create(name=listtext['name'],username=listtext['username'],password=listtext['password'],
        workPermitNumber=listtext['workPermitNumber'],workPermitPassword=listtext['workPermitPassword'],login_jwt=loginjwt)
        if nurse:
            obj = Head2Nurse.objects.create(nurseWorkPermitNumber=listtext['workPermitNumber'],headNurseWorkPermitNumber=idhead)
            if obj == None:
                returnjson = {'state':'400','message':'head to nurse create fail'}
                print('nursemanage.护士长护士对应关系创建失败：')
            else:
                returnjson = {'state':'200','data':[]}
                print(returnjson)
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'nurse create fail'}
            print('nursemanage.护士创建失败：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
    elif request.method == "PUT":
        qstr = request.META['QUERY_STRING']
        workPermitNumber = parse.unquote(qstr[qstr.find('=')+1:])
        print('nursemanagePUT:',workPermitNumber)
        nurse = NurseInfo.objects.filter(workPermitNumber=workPermitNumber)
        loginjwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        print(loginjwt)
        if nurse:
            listtext = json.loads(request.body)
            print(listtext)
            name = listtext['name']
            username = listtext['username']
            password = listtext['password']
            nurse.update(name=name,username=username,password=password)
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such nurse'}
            print('nursemanage.护士不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
    elif request.method == "DELETE":
        qstr = request.META['QUERY_STRING']
        workPermitNumber = parse.unquote(qstr[qstr.find('=')+1:])
        print('nursemanageDELETE:',workPermitNumber)
        nurse = NurseInfo.objects.filter(workPermitNumber=workPermitNumber)
        if nurse:
            nurse.delete()
            Head2Nurse.objects.filter(nurseWorkPermitNumber=workPermitNumber).delete()
            NurseToPaientInfo.objects.filter(nurseWorkPermitNumber=workPermitNumber).delete()
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such nurse'}
            print('nursemanage.护士不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
   
def inspectionpage(request):
    if request.method == "GET":
        inspectiondata = {}
        try:
            username = request.get_full_path().split("?")[1].split('&')[0].split("=")[1]
            jwt = request.get_full_path().split("?")[1].split('&')[1].split("=")[1]
            print("receive jwt: ",jwt)
            print("receive username: ",username)
            if username == "" or jwt == "" or jwt == "0":
                return redirect("/")  
        except:
            return redirect("/") 
        idhead = HeadNurseInfo.objects.filter(username=username)[0].workPermitNumber
        try:
            objs = Head2Nurse.objects.filter(headNurseWorkPermitNumber=idhead)
            if objs[0].nurseWorkPermitNumber:
                print(objs[0].nurseWorkPermitNumber)
                pass
        except IndexError:
            print('nursemanagement.get')
            returnjson = {'state':'400','message':'该护士长没有任何护士'}
        for obj in objs:
            obj = NurseInfo.objects.filter(workPermitNumber=obj.nurseWorkPermitNumber)[0]
            inspections = InspectionReports.objects.filter(idNurse=obj.workPermitNumber)
            for obj in inspections:
                inspectiondata[str(obj.id)] = {
                    "idNurse":obj.idNurse,
                    "location":obj.location,
                    "inspectionInfo":obj.inspectionInfo,
                    "inspectionDateTime":obj.inspectionDateTime
                }
        timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))            
        return render(request,"inspectionpage.html",{"inspectiondata":inspectiondata,"username":username,"time":timenow})
    elif request.method == "POST":
        listtext = json.loads(request.body)
        print(listtext)
        login_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idhead = HeadNurseInfo.objects.filter(login_jwt=login_jwt)[0].workPermitNumber
        idNurse = listtext['idNurse']
        obj = Head2Nurse.objects.filter(nurseWorkPermitNumber=idNurse,headNurseWorkPermitNumber=idhead)
        try:
            if obj[0]:
                pass
        except IndexError:
            returnjson = {'state':'400','message':'this headNurse do not have such nurse'}
            return HttpResponse(json.dumps(returnjson))
        obj = InspectionReports.objects.create(idNurse=listtext['idNurse'],location=listtext['location'],
        inspectionInfo=listtext['inspectionInfo'],inspectionDateTime=listtext['inspectionDateTime'])
        if obj == None :
            returnjson = {'state':'400','message':'add inspection report failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
    elif request.method == "PUT":
        print(request.get_full_path())
        text1 = request.get_full_path().split('?')[1]
        text2 = text1.split('&')
        idNurse = text2[0].split('=')[1]
        dateTime = parse.unquote(text2[1].split('=')[1])
        inspection = InspectionReports.objects.filter(idNurse=idNurse,inspectionDateTime=dateTime)
        if inspection:
            listtext = json.loads(request.body)
            print(listtext)
            location = listtext['location']
            inspectionInfo = listtext['inspectionInfo']
            inspection.update(location=location,inspectionInfo=inspectionInfo)
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such inspectionreport'}
            print('inspectionpage.巡视记录不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
    elif request.method == "DELETE":
        print(request.get_full_path())
        text1 = request.get_full_path().split('?')[1]
        text2 = text1.split('&')
        idNurse = text2[0].split('=')[1]
        dateTime = parse.unquote(text2[1].split('=')[1])
        inspection = InspectionReports.objects.filter(idNurse=idNurse,inspectionDateTime=dateTime)
        if inspection:
            inspection.delete()
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such inspectionreport'}
            print('inspectionpage.巡视记录不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))

def hazardpage(request):
    if request.method == "GET":
        hazarddata = {}
        try:
            username = request.get_full_path().split("?")[1].split('&')[0].split("=")[1]
            jwt = request.get_full_path().split("?")[1].split('&')[1].split("=")[1]
            print("receive jwt: ",jwt)
            print("receive username: ",username)
            if username == "" or jwt == "" or jwt == "0":
                return redirect("/")  
        except:
            return redirect("/")   
        idhead = HeadNurseInfo.objects.filter(login_jwt=jwt)[0].workPermitNumber
        try:
            objs = Head2Nurse.objects.filter(headNurseWorkPermitNumber=idhead)
            if objs[0].nurseWorkPermitNumber:
                print(objs[0].nurseWorkPermitNumber)
                pass
        except IndexError:
            print('nursemanagement.get')
            returnjson = {'state':'400','message':'该护士长没有任何护士'}
        for obj in objs:
            obj = NurseInfo.objects.filter(workPermitNumber=obj.nurseWorkPermitNumber)[0]
            hazards = HazardReports.objects.filter(idNurse=obj.workPermitNumber)
            for obj in hazards:
                hazarddata[str(obj.id)] = {
                    "idNurse":obj.idNurse,
                    "location":obj.location,
                    "hazardInfo":obj.hazardInfo,
                    "hazardDateTime":obj.hazardDateTime
                }
        timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))            
        return render(request,"hazardpage.html",{"hazarddata":hazarddata,"username":username,"time":timenow})
    elif request.method == "POST":
        listtext = json.loads(request.body)
        print('hazard.POST',listtext)
        login_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        idhead = HeadNurseInfo.objects.filter(login_jwt=login_jwt)[0].workPermitNumber
        idNurse = listtext['idNurse']
        obj = Head2Nurse.objects.filter(nurseWorkPermitNumber=idNurse,headNurseWorkPermitNumber=idhead)
        try:
            if obj[0]:
                pass
        except IndexError:
            returnjson = {'state':'400','message':'this headNurse do not have such nurse'}
            return HttpResponse(json.dumps(returnjson))
        obj = HazardReports.objects.create(idNurse=listtext['idNurse'],location=listtext['location'],
        hazardInfo=listtext['hazardInfo'],hazardDateTime=listtext['hazardDateTime'])
        print(obj)
        print(obj == None)
        if obj == None :
            returnjson = {'state':'400','message':'add hazard report failed'}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'200','data':[]}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
    elif request.method == "PUT":
        print(request.get_full_path())
        text1 = request.get_full_path().split('?')[1]
        text2 = text1.split('&')
        idNurse = text2[0].split('=')[1]
        dateTime = parse.unquote(text2[1].split('=')[1])
        hazard = HazardReports.objects.filter(idNurse=idNurse,hazardDateTime=dateTime)
        if hazard:
            listtext = json.loads(request.body)
            print(listtext)
            location = listtext['location']
            hazardInfo = listtext['hazardInfo']
            hazard.update(location=location,hazardInfo=hazardInfo)
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such hazardreport'}
            print('hazardpage.隐患记录不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
    elif request.method == "DELETE":
        print(request.get_full_path())
        text1 = request.get_full_path().split('?')[1]
        text2 = text1.split('&')
        idNurse = text2[0].split('=')[1]
        dateTime = parse.unquote(text2[1].split('=')[1])
        hazard = HazardReports.objects.filter(idNurse=idNurse,hazardDateTime=dateTime)
        if hazard:
            hazard.delete()
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such hazardreport'}
            print('hazardpage.隐患记录不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))


class nurseGroups(View):
    def get(self,request,nurse_id): # 获取
        return HttpResponse("get nurseinfo")

    def post(self,request,nurse_id): # 增加
        return HttpResponse("add nurseinfo")

    def put(self,request,nurse_id): # 修改
        return HttpResponse("change nurseinfo")

    def delete(self,request,nurse_id): # 删除
        return HttpResponse("delete nurseinfo")

class headNurseGroups(View):
    def get(self,request,headNurse_id): # 获取
        objs = NurseInfo.objects.all()
        nursedata = {}
        for obj in objs:
            nursedata[str(obj.id)] = {
                "headNurseName":obj.name,
                "headNurseworkPermitNumber": obj.workPermitNumber,
                "headNurseworkPermitPassword":obj.workPermitPassword,
                "username":obj.username,
                "password":obj.password
            }
        try:
            username = request.get_full_path().split("?")[1].split("=")[1]
            if username != "" :
                username = username+","
            else:
                username = ""
        except:
            username = ""  
        timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("!!!!!!!!!11")
        print(nursedata)
        print("!!!!!!!!!11")
        return render(request,"headnursemanagementpage.html",{"headnursedata":nursedata,"username":username,"time":timenow})
    def post(self,request,headNurse_id): # 增加
        print(request.method)
        listtext = json.loads(request.body)
        print(listtext)
        loginjwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        print(loginjwt)
        nurse = HeadNurseInfo.objects.create(name=listtext['name'],username=listtext['username'],password=listtext['password'],
        workPermitNumber=listtext['workPermitNumber'],workPermitPassword=listtext['workPermitPassword'],login_jwt=loginjwt)
        if nurse:
            returnjson = {'state':'200','data':[]}
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'headnurse create fail'}
            print('headnursemanage.护士长创建失败：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))

    def put(self,request,headNurse_id): # 修改
        qstr = request.META['QUERY_STRING']
        workPermitNumber = parse.unquote(qstr[qstr.find('=')+1:])
        print('headnursemanagePUT:',workPermitNumber)
        nurse = HeadNurseInfo.objects.filter(workPermitNumber=workPermitNumber)
        if nurse:
            listtext = json.loads(request.body)
            print(listtext)
            name = listtext['name']
            username = listtext['username']
            password = listtext['password']
            nurse.update(name=name,username=username,password=password)
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such headnurse'}
            print('headnursemanage.护士不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))

    def delete(self,request,headNurse_id): # 删除
        qstr = request.META['QUERY_STRING']
        workPermitNumber = parse.unquote(qstr[qstr.find('=')+1:])
        print('headnursemanageDELETE:',workPermitNumber)
        nurse = HeadNurseInfo.objects.filter(workPermitNumber=workPermitNumber)
        if nurse:
            nurse.delete()
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such headnurse'}
            print('headnursemanage.护士不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))