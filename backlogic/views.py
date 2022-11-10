from django.shortcuts import render, HttpResponse
from backlogic.models import NurseInfo
from backlogic.jwt import generate_jwt,decode_jwt
import jwt
import json


# Create your views here.
def test(request):
    return HttpResponse("丁真测你们码")

def sqltest(request):
    NurseInfo.objects.all().delete()
    return HttpResponse("成功")

def register(request):
    if request.method == 'POST':
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

        obj = NurseInfo.objects.filter(workPermitNumber=workPermitNumber)
        if obj ==None :
            returnjson = {'state':'register failed'}
            return HttpResponse(json.dumps(returnjson))
        else:
            obj.update(workPermitNumber = workPermitNumber,workPermitPassword = workPermitNumber,username = )
            returnjson = {'state':'register success'}
            return HttpResponse(json.dumps(returnjson))
    else:
        return HttpResponse("丁真测你们码")

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        storejwt = data['login_jwt']
        #验证用户名密码 username, password
        disk2 = decode_jwt(storejwt)
        print(disk2)

        returnjwt = generate_jwt(disk2)
        print(returnjwt)
        returndisk = {'jwt':returnjwt}
        return HttpResponse(json.dumps(returndisk))
    else:
        return HttpResponse("丁真测你们码")
