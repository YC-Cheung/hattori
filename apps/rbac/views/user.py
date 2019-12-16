from django.contrib.auth import get_user_model, authenticate

from common.api.base import BaseResponse
from common.api.exceptions import AuthFailedException
from common.auth import generate_token
from common.custom import BaseViewSet, BaseAPIView, AuthAPIView
from common.enums import JwtType
from rbac.serializers import UserSerializers

User = get_user_model()


class UserViewSet(BaseViewSet):
    """
    用户管理：增删改查
    """

    queryset = User.objects.all()
    serializer_class = UserSerializers


class UserAuthView(BaseAPIView):
    """
    登录
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthFailedException(message='用户名或密码错误')

        token = generate_token(uid=user.id, type=JwtType.ADMIN.value)
        return BaseResponse(data={
            'user': UserSerializers(user).data,
            'token': token,
        })


class UserInfoView(AuthAPIView):
    """
    用户信息
    """

    def get(self, request):
        user = request.user
        return BaseResponse(data=UserSerializers(user).data)
