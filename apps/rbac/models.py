from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    """
    角色
    """

    name = models.CharField(verbose_name='角色', max_length=50, unique=True)
    permissions = models.ManyToManyField('Perm', verbose_name='权限', blank=True)
    menus = models.ManyToManyField('Menu', verbose_name='菜单', blank=True)
    desc = models.CharField(verbose_name='描述', max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)


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
        (DELETE, 'delete'),
    ]

    name = models.CharField(verbose_name='权限名', max_length=50, unique=True)
    slug = models.CharField(verbose_name='权限标识', max_length=50, unique=True)
    method = models.CharField(verbose_name='请求方法', max_length=50, choices=METHOD_CHOICES, default=ANY)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)


class Menu(models.Model):
    """
    菜单
    """

    pid = models.ForeignKey('self', verbose_name='父级菜单', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(verbose_name='菜单名', max_length=50, unique=True)
    title = models.CharField(verbose_name='标题', max_length=50)
    icon = models.CharField(verbose_name='图标', max_length=50, blank=True, null=True)
    path = models.CharField(verbose_name='链接路径', max_length=150, blank=True, null=True)
    component = models.CharField(verbose_name='组件', max_length=50)
    is_show = models.BooleanField(verbose_name='是否显示', default=True)
    is_cache = models.BooleanField(verbose_name='是否缓存', default=False)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)


class User(AbstractUser):
    """
    管理员
    """

    roles = models.ManyToManyField('Role', verbose_name='角色', blank=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
