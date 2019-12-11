from django.urls import path, include
from rest_framework import routers

from rbac.views import user

router = routers.SimpleRouter()
router.register(r'users', user.UserViewSet, base_name='users')

urlpatterns = [
    path('', include(router.urls)),
]
