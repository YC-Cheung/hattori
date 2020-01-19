import logging

from django.http import JsonResponse
from jwt import DecodeError, ExpiredSignatureError, InvalidAlgorithmError
from rest_framework import status

from common.auth import bearer_token, verify_token

logger = logging.getLogger(__name__)


class JWTAuthenticationMiddleware:
    """
    JWT 认证中间件
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.payload = None
        token = bearer_token(request)
        if token:
            try:
                payload = verify_token(token)
                request.payload = payload
            except DecodeError as e:
                logger.exception(e)
                request.payload = None
            except ExpiredSignatureError as e:
                return JsonResponse(
                    data={'code': 4001, 'msg': '登录已失效，请重新登录', 'data': None},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except InvalidAlgorithmError as e:
                return JsonResponse(
                    data={'code': 4001, 'msg': '认证信息不合法', 'data': None},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        return self.get_response(request)
