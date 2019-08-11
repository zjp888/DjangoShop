from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
"""中间件元类，定义所有的中间件"""

class MiddlewareTest(MiddlewareMixin):

    def process_request(self,request):
        """
        :param request: 视图没有处理的请求
        :return
        """
        print("这是process_request请求")

    def process_view(self,request,view_func,view_args,view_kwargs):
        """
        :param request: 视图没有处理的请求
        :param view_func: 视图函数
        :param view_args: 视图函数的参数，元组形式
        :param view_kwargs:视图函数的参数，字典形式
        :return:
        """
        print("这是process_view请求")

    def process_exception(self,request,exception):
        """

        :param request: 视图的处理请求
        :param exception: 错误
        :return:
        """
        print("这是process_exception")

    def process_template_response(self,request,response):

        print("i am response")
        return response

    def process_response(self,request,response):
        print("这是process_response请求")
        return response




