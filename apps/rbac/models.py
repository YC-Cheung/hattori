from django.db import models
from django.contrib.auth.models import AbstractUser

from common.middleware.global_request import get_request
from rbac.mixins import ModelTreeMixin
from rbac.utils import perm_inspector, menu_tree_to_vue


class Role(models.Model):
    """
    角色
    """

    name = models.CharField(verbose_name='角色', max_length=50)
    slug = models.CharField(verbose_name='标识', max_length=50, unique=True)
    perms = models.ManyToManyField('Perm', related_name='roles', verbose_name='权限', blank=True)
    menus = models.ManyToManyField('Menu', related_name='roles', verbose_name='菜单', blank=True)
    desc = models.CharField(verbose_name='描述', max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Perm(models.Model):
    """
    权限
    """

    ANY = '*'
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'

    METHOD_CHOICES = [
        (ANY, 'ANY'),
        (GET, 'GET'),
        (POST, 'POST'),
        (PUT, 'PUT'),
        (PATCH, 'PATCH'),
        (DELETE, 'DELETE'),
    ]

    name = models.CharField(verbose_name='权限名', max_length=50)
    slug = models.CharField(verbose_name='权限标识', max_length=50, unique=True)
    method = models.CharField(verbose_name='请求方法', max_length=50, choices=METHOD_CHOICES, default=ANY)
    path = models.CharField(verbose_name='请求路径', max_length=200, null=True, blank=True)
    desc = models.TextField(verbose_name='权限描述', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Menu(ModelTreeMixin):
    """
    菜单
    """

    parent = models.ForeignKey('self', verbose_name='父级菜单', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(verbose_name='菜单名', max_length=50, unique=True)
    title = models.CharField(verbose_name='标题', max_length=50)
    icon = models.CharField(verbose_name='图标', max_length=50, blank=True, null=True)
    path = models.CharField(verbose_name='链接路径', max_length=150, blank=True, null=True)
    component = models.CharField(verbose_name='组件', max_length=50)
    is_show = models.BooleanField(verbose_name='是否显示', default=True)
    is_cache = models.BooleanField(verbose_name='是否缓存', default=False)
    sort = models.IntegerField(verbose_name='排序', default=0, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def get_parent_field(self):
        return 'parent_id'

    def all_nodes(self):
        nodes = self.get_manager().prefetch_related('roles').all()
        return nodes

    def ignore_tree_node(self, node):
        role_slugs = [role.slug for role in node.roles.all()]
        is_ignore = perm_inspector.check_role(get_request().user, role_slugs) is False
        return is_ignore


class User(AbstractUser):
    """
    管理员
    """

    roles = models.ManyToManyField('Role', verbose_name='角色', blank=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    @property
    def role_slugs(self):
        roles = self.roles.all()
        if roles is None:
            return []
        return [role.slug for role in roles]

    @property
    def perm_slugs(self):
        perms = self.roles.filter(perms__slug__isnull=False).values('perms__slug').distinct()
        if not perms:
            return []

        return [p['perms__slug'] for p in perms]

    @property
    def info(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_active': self.is_active,
            'roles': self.role_slugs,
            'perms': self.perm_slugs,
            'menus': menu_tree_to_vue(Menu().to_tree()),
        }
