from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from common.custom import DynamicFieldsModelSerializer
from rbac.models import Role, Perm, Menu

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    """
    管理员
    """

    username = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已被使用')],
        error_messages={
            'blank': '用户名不能为空',
            'required': '请输入用户名',
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    roles = serializers.SerializerMethodField()

    # role_ids = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True, many=True)

    def get_roles(self, obj):
        return [{'id': i.id, 'name': i.name, 'slug': i.slug} for i in obj.roles.all()]
        # return obj.roles.values('id', 'name', 'slug')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        instance = super(UserSerializers, self).create(validated_data)
        return instance
        # role_ids = validated_data.pop('role_ids')
        # if role_ids:
        #     instance.roles.set(role_ids)
        # return instance

    def update(self, instance, validated_data):
        validated_data.pop('username')
        password = validated_data.get('password', None)
        if password is not None:
            validated_data['password'] = make_password(password)
        instance = super(UserSerializers, self).update(instance, validated_data)
        return instance
        # role_ids = validated_data.pop('role_ids')
        # if role_ids:
        #     instance.roles.set(role_ids)
        # return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_active', 'roles')


class RoleSerializers(serializers.ModelSerializer):
    """
    角色
    """

    name = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            'blank': '角色名称不能为空',
            'required': '请输入角色名称',
        }
    )
    slug = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=Role.objects.all(), message='角色标识已被使用')],
        error_messages={
            'blank': '角色标识不能为空',
            'required': '请输入角色标识',
        }
    )

    class Meta:
        model = Role
        fields = ('id', 'name', 'slug', 'desc')


class RoleWithAllFieldsSerializer(DynamicFieldsModelSerializer):
    """
    角色 带全部字段
    """

    perms = serializers.SerializerMethodField()
    menus = serializers.SerializerMethodField()

    def get_perms(self, obj):
        return [{'id': i.id, 'name': i.name, 'slug': i.slug} for i in obj.perms.all()]

    def get_menus(self, obj):
        return [{'id': i.id, 'name': i.name, 'title': i.title} for i in obj.menus.all()]

    class Meta:
        model = Role
        fields = ('id', 'name', 'slug', 'desc', 'perms', 'menus', 'created_at', 'updated_at')


class PermSerializers(serializers.ModelSerializer):
    """
    权限
    """

    name = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            'blank': '权限名称不能为空',
            'required': '请输入权限名称',
        }
    )
    slug = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=Perm.objects.all(), message='权限标识已被使用')],
        error_messages={
            'blank': '权限标识不能为空',
            'required': '请输入权限标识',
        }
    )

    class Meta:
        model = Perm
        fields = ('id', 'name', 'slug', 'desc', 'method', 'path')


class PermWithAllFieldsSerializer(DynamicFieldsModelSerializer):
    """
    权限 带全部字段
    """

    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return [{'id': i.id, 'name': i.name, 'slug': i.slug} for i in obj.roles.all()]

    class Meta:
        model = Perm
        fields = ('id', 'name', 'slug', 'desc', 'method', 'path', 'roles', 'created_at', 'updated_at')


class MenuSerializers(serializers.ModelSerializer):
    """
    菜单
    """

    name = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=Perm.objects.all(), message='菜单名称已被使用')],
        error_messages={
            'blank': '菜单名称不能为空',
            'required': '请输入菜单名称',
        }
    )
    title = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            'blank': '菜单标题不能为空',
            'required': '请输入标题名称',
        }
    )
    path = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            'blank': 'URL 路径不能为空',
            'required': '请输入 URL 路径',
        }
    )
    component = serializers.CharField(
        required=True,
        max_length=200,
        error_messages={
            'blank': '组件名称不能为空',
            'required': '请输入组件名称',
        }
    )

    class Meta:
        model = Menu
        fields = ('id', 'parent', 'name', 'title', 'icon', 'path', 'component', 'is_show', 'is_cache')


class MenuWithAllFieldsSerializers(DynamicFieldsModelSerializer):
    """
    菜单 全字段
    """

    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return [{'id': i.id, 'name': i.name, 'slug': i.slug} for i in obj.roles.all()]

    class Meta:
        model = Menu
        fields = (
            'id', 'parent', 'name', 'title', 'icon', 'path', 'component', 'is_show', 'is_cache', 'roles', 'created_at',
            'updated_at')
