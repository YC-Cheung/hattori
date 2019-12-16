from common.custom import BaseViewSet
from rbac.models import Perm
from rbac.serializers import PermSerializers


class PermViewSet(BaseViewSet):
    """
    权限 增删改查
    """

    queryset = Perm.objects.all()
    serializer_class = PermSerializers
    filter_fields = ['name']
    search_fields = ['name', 'slug']
    ordering_fields = ['id']
