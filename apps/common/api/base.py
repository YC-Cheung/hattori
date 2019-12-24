from rest_framework import status
from rest_framework.response import Response


class BaseResponse(Response):

    def __init__(self, code=0, msg='', data: dict = None, status_code: int = status.HTTP_200_OK):
        response_data = {
            'code': code,
            'msg': msg,
            'data': data
        }
        super(BaseResponse, self).__init__(data=response_data, content_type='application/json',
                                           status=status_code)
