from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from common.auth.authentication import BackendAuthentication


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        excludes = kwargs.pop('excludes', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif excludes is not None:
            removed = set(excludes)
            for field_name in removed:
                self.fields.pop(field_name)


class CustomJsonRenderer(JSONRenderer):
    """
    自定义响应模版
    """

    SUCCESS_MESSAGE = 'Success.'
    SUCCESS_CODE = 0

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                msg = data.pop('msg', self.SUCCESS_MESSAGE)
                code = data.pop('code', self.SUCCESS_CODE)
            else:
                msg = self.SUCCESS_MESSAGE
                code = self.SUCCESS_CODE
            response = renderer_context['response']
            response.status_code = response.status_code or response.get('status_code', status.HTTP_200_OK)

            if data is not None:
                data = data.pop('data', data)

            res = {
                'code': code,
                'msg': msg,
                'data': data,
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)


class BaseSetPagination(PageNumberPagination):
    """
    分页设置 基类
    """

    page_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data,
        })


class StandardResultsSetPagination(BaseSetPagination):
    """
    标准分页设置
    """

    page_size = 50
    max_page_size = 500


class LargeResultsSetPagination(BaseSetPagination):
    """
    Large 分页设置
    """

    page_size = 1000
    max_page_size = 10000


class BaseViewSet(viewsets.ModelViewSet):
    """
    基础 ViewSet
    """

    pagination_class = StandardResultsSetPagination
    renderer_classes = [CustomJsonRenderer, BrowsableAPIRenderer]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]


class AuthViewSet(BaseViewSet):
    """
    登录认证 ViewSet
    """

    authentication_classes = [BackendAuthentication]


class BaseAPIView(APIView):
    """
    API 基类
    """


class AuthAPIView(BaseAPIView):
    """
    登录认证
    """

    authentication_classes = [BackendAuthentication]
