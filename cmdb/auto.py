#coding=utf-8
__author__ = 'DELL'
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from tools.tools import *
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tools.zabbix.sum_result import *
#def hostinfo_index(request):
#    result=cmdb_auto_info.objects.all()
#    return render_to_response('hostinfo_index.html',{'cons':result})


def hostinfo_index(request):
    cons = cmdb_auto_info.objects.all()
    #print cons
    return render_to_response('hostinfo_index.html', {"contacts": cons})

def zyuser(request):
    if request.GET.has_key('ip'):
        ip=request.GET['ip']
        a=get_result(ip)
        if a:
            memoryinfo=a['memoryfree']['value']
            memclock=a['memoryfree']['clock']
            cpuinfo=a['cpu']['value']
            cpuclock=a['cpu']['clock']
            return render_to_response('zyuser.html',{"memoryinfo":memoryinfo,"memclock":memclock,"cpuinfo":cpuinfo,"cpuclock":cpuclock,"ip":ip})
        else:
            return HttpResponse("主机没有监控")
    else:
        return render_to_response('zyuser.html')



