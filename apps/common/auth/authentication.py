from django.contrib.auth import get_user_model
from jwt import ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import WrappedAttributeError

from common.api.exceptions import AuthFailedException, CrossDomainException, AdminUserForbiddenException
from common.enums import JwtType

User = get_user_model()


class BackendAuthentication(BaseAuthentication):
    """
    管理后台认证
    """

    def authenticate(self, request):
        try:
            payload = request.payload
            if payload is None:
                raise AuthFailedException(message='请登录')
        except WrappedAttributeError:
            raise AuthFailedException(message='请登录')

        if request.payload.get('type') != JwtType.ADMIN.value:
            raise CrossDomainException()

        try:
            uid = payload.get('uid')
            user = User.objects.prefetch_related('roles').get(id=uid)
        except User.DoesNotExist:
            raise AuthFailedException(message='请登录')
        if not user.is_active:
            raise AdminUserForbiddenException(message='账号已被禁用，请联系管理员')
        return user, user.id
