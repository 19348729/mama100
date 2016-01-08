#coding=utf-8
__author__ = 'DELL'
from django.http import HttpResponse
def must_admin(func):
    def check_admin(request):
        if request.user.is_superuser:
            return func(request)
        else:
             return HttpResponse("没有权限噢！！")
    return check_admin
