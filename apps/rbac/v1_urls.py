from django.urls import path, include
from rest_framework import routers

from rbac.views import user, role, perm, menu

router = routers.SimpleRouter()
router.register(r'users', user.UserViewSet, base_name='users')
router.register(r'roles', role.RoleViewSet, base_name='roles')
router.register(r'perms', perm.PermViewSet, base_name='perms')
router.register(r'menus', menu.MenuViewSet, base_name='menus')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', user.UserAuthView.as_view()),
    path('auth/info/', user.UserInfoView.as_view()),
]
