from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.api.base import BaseResponse
from common.api.exceptions import AuthFailedException, APIException
from common.auth import generate_token
from common.custom import BaseAPIView, AuthAPIView, RbacViewSet
from common.enums import JwtType
from rbac.serializers import UserSerializers

User = get_user_model()


class UserViewSet(RbacViewSet):
    """
    用户管理：增删改查
    """

    queryset = User.objects.prefetch_related('roles').all()
    serializer_class = UserSerializers

    @action(methods=['post'], detail=True, url_path='roles')
    def set_roles(self, request, pk=None):
        user = self.get_object()
        roles = request.data.get('roles')
        user.roles.set(roles)
        return BaseResponse()

    def create(self, request, *args, **kwargs):
        """
        创建用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        password = request.data.get('password')
        if password is not None:
            confirm_password = request.data.get('confirm_password')
            if password != confirm_password:
                raise APIException(message='两次输入的密码不一致')
        else:
            password = settings.DEFAULT_PASSWORD

        request.data['password'] = password
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        password = request.data.get('password')
        if password is not None:
            if password:
                confirm_password = request.data.get('confirm_password')
                if password != confirm_password:
                    raise APIException(message='两次输入的密码不一致')
            else:
                request.data.pop('password')

        return super().update(request, *args, **kwargs)


class UserAuthView(BaseAPIView):
    """
    登录
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise APIException(message='用户名或密码错误', status_code=status.HTTP_200_OK)

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
        return BaseResponse(data=user.info)
