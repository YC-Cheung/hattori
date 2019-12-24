import re

from django.conf import settings
from rest_framework.permissions import BasePermission

from rbac.utils import perm_inspector


class RbacPermission(BasePermission):
    """
    rbac 权限控制
    """

    ALL_ALLOW_SLUG = ['*']
    ALL_ALLOW_METHOD = ['*']

    @classmethod
    def get_perms(cls, user):
        """
        获取当前请求用户的权限
        :param user:
        :return:
        """

        try:
            perms = user.roles.values(
                'perms__slug',
                'perms__method',
                'perms__path',
            ).distinct()

            return [(p['perms__slug'], p['perms__method'], p['perms__path']) for p in perms]
        except AttributeError:
            return []

    @classmethod
    def is_white_list(cls, path_info):
        """
        是否在请求白名单中
        :param path_info:
        :return:
        """

        white_list = settings.RBAC_URL_WHITE_LIST
        if not white_list:
            return False

        if path_info in white_list:
            return True

        return False

    @classmethod
    def is_pass_through(cls, request):
        """
        路由判断
        :param request:
        :return:
        """

        perms = cls.get_perms(request.user)
        if not perms:
            return False

        path_info = request.path_info
        request_method = request.method.lower()
        allow_method = [request_method] + cls.ALL_ALLOW_METHOD

        for slug, method, path in perms:
            if slug in cls.ALL_ALLOW_SLUG:
                return True

            if (method in allow_method) and re.match(path, path_info):
                return True

        return False

    def has_permission(self, request, view):
        if perm_inspector.is_super_admin(request.user):
            return True

        if self.is_white_list(request):
            return True

        if self.is_pass_through(request):
            return True

        return False
