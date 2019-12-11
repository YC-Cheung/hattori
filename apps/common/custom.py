from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response


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
            response.status_code = response.get('status_code', status.HTTP_200_OK)
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
