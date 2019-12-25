from rest_framework import status


class APIException(Exception):
    """
    通用 API 异常
    """

    def __init__(self, message='', code=4999, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        self.status_code = status_code

    @property
    def data(self):
        return {
            'err_code': self.code,
            'msg': self.message,
        }


class AuthFailedException(APIException):
    """
    登录认证失败异常
    """

    def __init__(self, message='Unauthenticated.', code=4001, status_code=status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, code, status_code)


class CrossDomainException(AuthFailedException):
    """
    Token 跨域认证
    """

    def __init__(self, message='Invalid token.', code=4003, status_code=status.HTTP_403_FORBIDDEN):
        super().__init__(message, code, status_code)


class AdminUserForbiddenException(AuthFailedException):
    """
    后台管理员被禁用
    """

    def __init__(self, message='You have been banned.', code=4003, status_code=status.HTTP_403_FORBIDDEN):
        super().__init__(message, code, status_code)
