from django.shortcuts import render, redirect
from django.views import View
import json
import os
# Create your views here.

def logpage(request):
    if request.method == "GET":
        return render(request,"logpage.html")
    
def mainpage(request):
    if request.method == "GET":
        return render(request,"mainpage.html")


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