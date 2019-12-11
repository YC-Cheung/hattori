from django.contrib.auth import get_user_model

from common.custom import BaseViewSet
from rbac.serializers import UserSerializers

User = get_user_model()


class UserViewSet(BaseViewSet):
    """
    用户管理：增删改查
    """

    queryset = User.objects.all()
    serializer_class = UserSerializers
