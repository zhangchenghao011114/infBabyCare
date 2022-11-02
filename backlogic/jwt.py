import time
import jwt  

secret = '1919810'
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

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token