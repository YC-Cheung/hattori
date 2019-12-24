from rest_framework.decorators import action

from common.api.base import BaseResponse
from common.custom import RbacViewSet
from rbac.models import Menu
from rbac.serializers import MenuSerializers
from rbac.utils import menu_tree_to_vue


class MenuViewSet(RbacViewSet):
    """
    菜单管理：增删改查
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializers
    filter_fields = ['name', 'title']
    search_fields = ['name', 'title']
    ordering_fields = ['id']

    @action(detail=False, methods=['get'], url_path='tree')
    def get_tree(self, request):
        """
        获取菜单树状图
        :param request:
        :return:
        """

        menus = Menu().to_tree()
        result = menu_tree_to_vue(menus)
        return BaseResponse(data=result)

    @action(detail=True, methods=['post'], url_path='roles')
    def set_roles(self, request, pk=None):
        """
        设置菜单角色
        :param request:
        :param pk:
        :return:
        """

        menu = self.get_object()
        roles = request.data.get('roles')
        menu.roles.set(roles)
        return BaseResponse()
