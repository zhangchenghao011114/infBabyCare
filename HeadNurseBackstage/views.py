from django.shortcuts import render, redirect, HttpResponse
from django.http import QueryDict
from HeadNurseBackstage.models import HeadNurseInfo
from backlogic.models import NurseInfo,InspectionReports,HazardReports
from backlogic.jwt import generate_jwt,decode_jwt,verify_jwt,decode_jwt_back
from django.views import View
import json
import os
from django.utils import timezone
import pytz
import time
# Create your views here.

nursedata = {"123456":{"NurseName":"丁真","NurseWorkPermitNumber":"123456","NurseWorkPermitPassword":"666",
                       "usrname":"瑞克五代","password":"测尼玛"},
             "1":{"NurseName":"王源","NurseWorkPermitNumber":"2","NurseWorkPermitPassword":"3",
                       "usrname":"5","password":"6"}}
inspectiondata = {"123456":{"idNurse":"123456","location":"四川理塘","inspectionInfo":"妈妈在给我充电子烟",
                       "inspectionDateTime":"2022/11/19 11:00"},
                  "1":{"idNurse":"123456","location":"四川理塘","inspectionInfo":"妈妈在给我充电子烟",
                       "inspectionDateTime":"2022/11/19 11:00"}}
hazarddata = {"123456":{"idNurse":"123456","location":"四川理塘","hazardInfo":"雪豹闭嘴",
                       "hazardDateTime":"2022/11/19 11:00"},
              "1":{"idNurse":"123456","location":"四川理塘","hazardInfo":"雪豹闭嘴",
                       "hazardDateTime":"2022/11/19 11:00"}}

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
            username = request.get_full_path().split("?")[1].split("=")[1]
            username = username+","
        except:
            username = ""        
            timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return render(request,"mainpage.html",{"username":username,"time":timenow})
    # elif request.method == "POST":
    #     return redirect("/")

def nursemanagementpage(request):
    if request.method == "GET":
        objs = NurseInfo.objects.all()
        nursedata = {}
        for obj in objs:
            nursedata[str(obj.id)] = {
                "NurseName":obj.name,
                "NurseWorkPermitNumber": obj.workPermitNumber,
                "NurseWorkPermitPassword":obj.workPermitPassword,
                "username":obj.username,
                "password":obj.password
            }
        try:
            username = request.get_full_path().split("?")[1].split("=")[1]
            username = username+","
        except:
            username = ""
        timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return render(request,"nursemanagementpage.html",{"nursedata":nursedata,"username":username,"time":timenow})
    elif request.method == "POST":
        print(request.method)
        listtext = json.loads(request.body)
        print(listtext)
        loginjwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
        print(loginjwt)
        nurse = NurseInfo.objects.create(name=listtext['name'],username=listtext['username'],password=listtext['password'],
        workPermitNumber=listtext['workPermitNumber'],workPermitPassword=listtext['workPermitPassword'],login_jwt=loginjwt)
        if nurse:
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'nurse create fail'}
            print('nursemanage.护士创建失败：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
    elif request.method == "PUT":
        qstr = request.META['QUERY_STRING']
        workPermitNumber = qstr[qstr.find('=')+1:]
        print('nursemanage:',workPermitNumber)
        nurse = NurseInfo.objects.filter(workPermitNumber=workPermitNumber)
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
        workPermitNumber = qstr[qstr.find('=')+1:]
        print('nursemanage:',workPermitNumber)
        nurse = NurseInfo.objects.filter(workPermitNumber=workPermitNumber)
        if nurse:
            nurse.delete()
            returnjson = {'state':'200','data':[]}
            return HttpResponse(json.dumps(returnjson))
        else:
            returnjson = {'state':'400','message':'no such nurse'}
            print('nursemanage.护士不存在：')
            print(returnjson)
            return HttpResponse(json.dumps(returnjson))
   
def inspectionpage(request):
    if request.method == "GET":
        objs = InspectionReports.objects.all()
        inspectiondata = {}
        for obj in objs:
            inspectiondata[str(obj.id)] = {
                "idNurse":obj.idNurse,
                "location":obj.location,
                "inspectionInfo":obj.inspectionInfo,
                "inspectionDateTime":obj.inspectionDateTime
        }
        return render(request,"inspectionpage.html",{"inspectiondata":inspectiondata})
    elif request.method == "POST":
        tmp =  request.POST.get("NurseWorkPermitNumber")
        print(request.POST)
        return redirect("/inspectionpage")

def hazardpage(request):
    if request.method == "GET":
        objs = HazardReports.objects.all()
        hazarddata = {}
        for obj in objs:
            hazarddata[str(obj.id)] = {
                "idNurse":obj.idNurse,
                "location":obj.location,
                "hazardInfo":obj.hazardInfo,
                "hazardDateTime":obj.hazardDateTime
        }
        return render(request,"hazardpage.html",{"hazarddata":hazarddata})
    elif request.method == "POST":
        print(request.POST)
        return redirect("/hazardpage")


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
        return HttpResponse("get headNurseinfo")

    def post(self,request,headNurse_id): # 增加
        return HttpResponse("add headNurseinfo")

    def put(self,request,headNurse_id): # 修改
        return HttpResponse("change headNurseinfo")

    def delete(self,request,headNurse_id): # 删除
        return HttpResponse("delete headNurseinfo")