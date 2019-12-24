import threading

GLOBAL_REQUEST_KEEPER = threading.local()


class GlobalRequestMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        GLOBAL_REQUEST_KEEPER.request = request
        try:
            return self.get_response(request)
        finally:
            del GLOBAL_REQUEST_KEEPER.request


def get_request():
    try:
        return GLOBAL_REQUEST_KEEPER.request
    except AttributeError:
        return None

# import threading
# from django.utils.deprecation import MiddlewareMixin
#
# threading_local = threading.local()
#
#
# class GlobalRequestMiddleware(MiddlewareMixin):
#     """
#     全局request中间件
#     """
#
#     @staticmethod
#     def process_request(request):
#         threading_local.request = request
#
#
# class GlobalRequest(object):
#
#     def __getattr__(self, item):
#         return getattr(getattr(threading_local, 'request', None), item, None)
#
#
# global_request = GlobalRequest()

# from django.utils.deprecation import MiddlewareMixin
#
#
# class GlobalRequestMiddleware(MiddlewareMixin):
#     __instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.__instance:
#             cls.__instance = object.__new__(cls)
#         return cls.__instance
#
#     def process_request(self, request):
#         GlobalRequestMiddleware.__instance = request
#
#     @classmethod
#     def get_request(cls):
#         return cls.__instance
#
#
# request = GlobalRequestMiddleware.get_request()

# from threading import current_thread
#
# class GlobalRequest(object):
#     _requests = {}
#
#     @staticmethod
#     def get_request():
#         try:
#             return GlobalRequest._requests[current_thread()]
#         except KeyError:
#             return None
#
#     def process_request(self, request):
#         GlobalRequest._requests[current_thread()] = request
#
#     def process_response(self, request, response):
#         # Cleanup
#         thread = current_thread()
#         try:
#             del GlobalRequest._requests[thread]
#         except KeyError:
#             pass
#         return response
#
# def get_request():
#     return GlobalRequest.get_request()
