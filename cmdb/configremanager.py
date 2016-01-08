#coding=utf-8
__author__ = 'Ben'
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tools.getdir import *
#from tools.tools import *
from models import *
import time
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tools.zabbix.sum_result import *
currentdate=time.strftime("%Y-%m-%d", time.localtime())
config_bak_folder='/config_bak/'
#def hostinfo_index(request):
#    result=cmdb_auto_info.objects.all()
#    return render_to_response('hostinfo_index.html',{'cons':result})
def networkdy_index(request):
    contacts=cmdb_networkdy.objects.all()
    return render_to_response('networkdy_index.html', {"contacts": contacts})

def get_file_info(request):
    req=request.GET
    file_name=req['file_name']
    print "bnnnn"
    print file_name
    f=open(file_name,'rb')
    file1=f.readlines()
    f.close()
    return HttpResponse(file1)

def config_info_commit(request):
    req=request.POST
    file_name=req['file_name']
    # file_name_new=file_name[::-1][:file_name[::-1].find('/')][::-1]
    file_name_new=file_name.split('/')[-1]
    print file_name
    comm='cp '+file_name+' '+config_bak_folder+file_name_new+currentdate
    os.popen(comm)
    try:
        f=open(file_name,'wb')
        context=req['filename_cont']
        f.write(context)
        f.close()
        return HttpResponse("You change file sucess!")
    except IOError:
        return HttpResponse("文件有问题")


def config_edit(request):
    req=request.GET
    print "#########%s#######"%req
    soft_name=req['soft_name']
    try:
        base_dir='/mama100/jenkins/deploy/patch/'
        find_dir=base_dir+soft_name
        find_dir_list=get_dir_file(find_dir)
        return render_to_response('config_edit.html',{'find_dir_list':find_dir_list})
    except OSError:
        return HttpResponse("没有此目录")


