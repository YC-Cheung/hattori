from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    """
    管理员 序列化
    """

    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active', 'roles', 'created_at', 'updated_at',)
