from django.shortcuts import render, redirect
from django.views import View
import json
import os
# Create your views here.

nursedata = {"123456":{"NurseName":"丁真","NurseWorkPermitNumber":"123456","NurseWorkPermitPassword":"666",
                       "NurseAge":"21","usrname":"瑞克五代","password":"测尼玛"}}
inspectiondata = {"123456":{"idNurse":"123456","location":"四川理塘","inspectionInfo":"妈妈在给我充电子烟",
                       "inspectionDateTime":"2022/11/19 11:00"}}
hazarddata = {"123456":{"idNurse":"123456","location":"四川理塘","hazardInfo":"雪豹闭嘴",
                       "hazardDateTime":"2022/11/19 11:00"}}

def logpage(request):
    if request.method == "GET":
        return render(request,"logpage.html")
    elif request.method == "POST":
        if request.POST.get("login") == "1": # 登录
            return redirect("/mainpage")
        elif request.POST.get("register") == "1": # 注册
            return redirect("/registerpage")
        
def registerpage(request):
    if request.method == "GET":
        return render(request,"registerpage.html")
    elif request.method == "POST":
        return redirect("/mainpage")
    
def mainpage(request):
    if request.method == "GET":
        return render(request,"mainpage.html",{"username":"李护士","time":"2022/11/19"})
    elif request.method == "POST":
        return redirect("/")

def nursemanagementpage(request):
    if request.method == "GET":
        # return render(request,"nursemanagementpage.html",{"username":"李护士","time":"2022/11/19"},{"nursedata":nursedata})
        return render(request,"nursemanagementpage.html",{"nursedata":nursedata})
    elif request.method == "POST":
        return redirect("/nursemanagementpage")
    
def inspectionpage(request):
    if request.method == "GET":
        # return render(request,"nursemanagementpage.html",{"username":"李护士","time":"2022/11/19"},{"nursedata":nursedata})
        return render(request,"inspectionpage.html",{"inspectiondata":inspectiondata})
    elif request.method == "POST":
        return redirect("/inspectionpage")
    
def hazardpage(request):
    if request.method == "GET":
        # return render(request,"nursemanagementpage.html",{"username":"李护士","time":"2022/11/19"},{"nursedata":nursedata})
        return render(request,"hazardpage.html",{"hazarddata":hazarddata})
    elif request.method == "POST":
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