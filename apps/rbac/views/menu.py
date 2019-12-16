from common.custom import BaseViewSet
from rbac.models import Menu
from rbac.serializers import MenuSerializers


class MenuViewSet(BaseViewSet):
    """
    角色管理：增删改查
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializers
    filter_fields = ['name', 'title']
    search_fields = ['name', 'title']
    ordering_fields = ['id']
