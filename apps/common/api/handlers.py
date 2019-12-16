from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import exception_handler

from common.api.base import BaseResponse
from common.api.exceptions import APIException


def get_error_message(exception):
    if isinstance(exception, str):
        return exception.capitalize()

    if isinstance(exception, list):
        for item in exception:
            return get_error_message(item)

    if isinstance(exception, dict):
        return get_error_message(exception[next(iter(exception))])

    if isinstance(exception, Exception):
        if hasattr(exception, 'detail'):
            return get_error_message(exception.detail)
        if hasattr(exception, 'message'):
            return get_error_message(exception.message)

    return exception.__str__()


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc:
    :param context:
    :return:
    """

    response = exception_handler(exc, context)
    view = context.get('view')

    if isinstance(exc, Http404) or isinstance(exc, NotFound):
        return BaseResponse(code=4999, msg='资源不存在', status_code=response.status_code)

    if isinstance(exc, ValidationError):
        return BaseResponse(code=4999, msg=get_error_message(exc), status_code=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, APIException):
        return BaseResponse(code=exc.code, msg=exc.message, status_code=status.HTTP_400_BAD_REQUEST)
