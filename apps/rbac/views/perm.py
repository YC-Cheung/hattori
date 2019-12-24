from rest_framework.decorators import action

from common.api.base import BaseResponse
from common.custom import RbacViewSet
from rbac.models import Perm
from rbac.serializers import PermSerializers


class PermViewSet(RbacViewSet):
    """
    权限 增删改查
    """

    queryset = Perm.objects.all()
    serializer_class = PermSerializers
    filter_fields = ['name']
    search_fields = ['name', 'slug']
    ordering_fields = ['id']

    @action(detail=True, methods=['post'], url_path='roles')
    def set_roles(self, request, pk=None):
        """
        设置权限角色
        :param request:
        :param pk:
        :return:
        """

        perm = self.get_object()
        roles = request.data.get('roles')
        perm.roles.set(roles)
        return BaseResponse()
