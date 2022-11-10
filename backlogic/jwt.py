import time
import jwt  

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

    token = jwt.encode(_payload, secret1, algorithm='HS256')
    return token

def decode_jwt(token):
    #token = content['login_jwt']#
    #signing_input, crypto_segment = content['login_jwt'].rsplit('.', 1)
    #header_segment, payload_segment = signing_input.split('.', 1)
    payload = jwt.decode(token,secret2,algorithms=['HS256'])
    return payload