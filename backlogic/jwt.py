import time
import jwt  
from backlogic.models import NurseInfo,PatientInfo

secret1 = '1919810'
secret2 = '紫者，妪也，紫大寿，强宴宾客于迷途家。肴即尽，取陈酒，觞诸宾。宾皆不敢，尽却之。唯天子许，饮三壶，大醉。紫甚欣慰，请起舞悦众宾。众思谢之恐死，苦不敢言。遂舞。笙箫起，笛音生，紫披发旖旎，自思艳绝。舞毕，遽顾问于客。客皆骇然称善。唯天子醉曰：“笑煞人，老妪何惺惺然作处子态!”鞭于庭。'
def generate_jwt(payload, expiry=None):
    """

    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :return: 生成jwt
    """
    if expiry is None:
        expiry = int(time.time()) + 60 *5

    _payload = {'exp': expiry}
    _payload.update(payload)
    #token = ''
    token = jwt.encode(_payload, secret1, algorithm='HS256')
    return token

def decode_jwt(token):
    payload = jwt.decode(token,secret2,algorithms=['HS256'])
    #payload = ''
    return payload

def decode_jwt_back(token):
    try:
        payload = jwt.decode(token,secret1,algorithms=['HS256'])
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        return False

def verify_jwt(token):
    obj = NurseInfo.objects.filter(login_jwt = token)
    try: 
        if obj[0].workPermitNumber:
            # print( obj[0].login_jwt)
            return obj[0].workPermitNumber
        else:
            print('工作证号不存在')
            return False
    except IndexError:
        return False


def remoteLoginVerification(request):
    # 获取该名护士照顾的所有病人的信息
    # 验证http请求head中的jwt
    verification_jwt = request.META['HTTP_LOGINJWT']  #规定jwt存在header的HTTP_LOGINJWT中
    print('patient2nurse:')
    print(verification_jwt)

    # 建议传过来的jwt是否可解码
    payload = decode_jwt_back(verification_jwt)
    if payload:
        pass
    else:
        return false
        # returnjson = {'state':'400','message':'登录状态异常,jwt不存在'}
        # return HttpResponse(json.dumps(returnjson))

    # 可解码的情况下，判断该jwt是否与数据库中的jwt相同，不同则说明这个jwt是被顶掉的
    idnurse = verify_jwt(verification_jwt)
    print(idnurse)
    if idnurse:
        return true       
    else:
        return false
