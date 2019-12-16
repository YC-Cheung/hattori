from common.custom import BaseViewSet
from rbac.models import Role
from rbac.serializers import RoleSerializers


class RoleViewSet(BaseViewSet):
    """
    角色管理：增删改查
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializers
    filter_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id']
