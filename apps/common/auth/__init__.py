import datetime

import jwt
from django.conf import settings

from apps.common.enums import JwtType


def bearer_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    if token:
        return token.split(' ')[1]
    return None


def generate_token(uid: int, type: int):
    """
    生成 token
    :param uid:
    :param type:
    :return:
    """

    token = jwt.encode({
        'uid': uid,
        'type': type,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_TTL)
    }, key=settings.SECRET_KEY)
    return token


def verify_token(token: str):
    """
    验证 token
    :param token:
    :return:
    """
    payload = jwt.decode(jwt=token, key=settings.SECRET_KEY)
    return payload
