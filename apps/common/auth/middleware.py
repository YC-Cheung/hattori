import logging

from jwt import DecodeError

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

        return self.get_response(request)
