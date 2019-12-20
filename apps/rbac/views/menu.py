from rest_framework.decorators import action

from common.api.base import BaseResponse
from common.custom import AuthViewSet
from rbac.models import Menu
from rbac.serializers import MenuSerializers
from rbac.utils import menu_tree_to_vue


class MenuViewSet(AuthViewSet):
    """
    角色管理：增删改查
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializers
    filter_fields = ['name', 'title']
    search_fields = ['name', 'title']
    ordering_fields = ['id']

    @action(detail=False, methods=['get'], url_path='tree')
    def get_tree(self, request):
        """
        设置角色菜单
        :param request:
        :return:
        """

        menus = Menu().to_tree()
        result = menu_tree_to_vue(menus)
        return BaseResponse(data=result)
