from django.shortcuts import render, HttpResponse
from backlogic.models import NurseInfo
from backlogic.jwt import generate_jwt
import jwt


# Create your views here.
def test(request):
    return HttpResponse("丁真测你们码")

def sqltest(request):
    NurseInfo.objects.all().delete()
    return HttpResponse("成功")

def login(request):
    if request.method == 'POST':
        content = request.get_json()
        asdjwt = generate_jwt({
            "username": 'asd',#content['username'],
            "passwrod": 'qwe',#content['password']
        })
        return jsonify({
            'result':'success',
            "jwt":jwt,
        })
        #print(asdjwt)
        #_payload = jwt.decode(asdjwt, "1919810", algorithms='HS256')
        #print(_payload)
        #return HttpResponse("丁真测你们码")
    else:
        return HttpResponse("丁真测你们码")
