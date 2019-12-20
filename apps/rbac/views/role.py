from rest_framework.decorators import action

from common.api.base import BaseResponse
from common.custom import AuthViewSet
from rbac.models import Role
from rbac.serializers import RoleSerializers


class RoleViewSet(AuthViewSet):
    """
    角色管理：增删改查
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializers
    filter_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id']

    @action(detail=True, methods=['post'], url_path='perms')
    def set_perms(self, request, pk=None):
        """
        设置角色权限
        :param request:
        :param pk:
        :return:
        """

        role = self.get_object()
        perms = request.data.get('perms')
        role.permissions.set(perms)
        return BaseResponse()

    @action(detail=True, methods=['post'], url_path='menus')
    def set_menus(self, request, pk=None):
        """
        设置角色菜单
        :param request:
        :param pk:
        :return:
        """

        role = self.get_object()
        menus = request.data.get('menus')
        role.menus.set(menus)
        return BaseResponse()
