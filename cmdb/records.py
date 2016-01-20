# -*- coding: utf-8 -*-
#coding=utf-8
__author__ = 'NICK'
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import *


##文件上传使用
import os
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
cur_date=datetime.datetime.now().strftime("%Y%m%d")
cur_date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
###分页使用
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

xiangmu=["","20150615平台系统监控项目","20150615日志归集检索项目","20150713妈妈100app首购项目","20150714妈妈100巧儿宜特卖推广活动","20150715集团优惠券配置V5.02","20150721秒杀项目","20150723优惠活动服务V1.0","20150729跨境电商平台","20150803预发布和生产环境自动化部署","20150805妈妈100刷脸活动","20150805帐务结算系统-微服务化改造","20150807商家中心APPV4.2->营销工具","20150810妈妈100APPV4.2","20150810平台优惠券配置V1.01","20150810百城百店专题活动"]
#from tools.tools import *
from tools.jenkins.jenkins_api import *
from models import *
import time,datetime
from tools.get_docker_info import get_host
from views import docker_maxport
from tools.get_docker_info import docker_create
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tools.ssh_run import *
from mama100.dockerweb.models import *


def records(request):
    apply_type='fault_env'
    if request.GET:
        apply_type=request.GET['apply_type']
        print type
        if apply_type == 'all':
            contacts=cmdb_operation_records.objects.all
        else:
            contacts=cmdb_operation_records.objects.filter(apply_type=apply_type)
            print contacts
    else:
        contacts=cmdb_operation_records.objects.filter(apply_type='fault_env')
    return render_to_response('records.html', {"contacts": contacts,"apply_type":apply_type})


def records_input(request):
    result=cmdb_project.objects.all()
    print result
    re_dict={}
    re_list=[]
    ####从数据库表中取出所有的项目名，放进字典为了去重
    for i in result:
        # i.soft_name
        re_dict[i.project_name]=i.soft_name
        ####把字典的KEY转化成列表
    for j in re_dict.keys():
        re_list.append(j)
    re_list.sort()
    print len(re_dict)
    return render_to_response('Operation_submitted.html',{'xiangmu':re_list})


def recordcommit(request):
    a=request.POST
    print a
    b=request.FILES
    print b
    apply_type=a['apply_type']
    auth=a['auth']
    record_con=a['record_con']

    project_name=a['project_name']
    run_con=a['run_con']
    run_env=a['run_env']
    files = request.FILES.getlist('file')

    # file_name= cur_date+'/'+str(b.get('file',None))
    http_name="http://192.168.234.139/upload/"
    # up_file= b.get('file')
    report=cmdb_operation_records()
    # re_txt=''

    report.apply_type=apply_type
    report.auth=auth
    report.project_name=project_name
    report.run_con=run_con
    report.record_con=record_con
    report.run_ok=1
    report.run_env=run_env
    report.insert_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_url_list=[]
    for f in files:
        file_name=os.path.join('/var/www/html/upload',cur_date,f.name)
        # print file_name
        if os.access(file_name, os.F_OK):####已存在先删除
            print "cunzi"
            os.remove(file_name)
        else:####不存在直接上传
            print "new"
        path=default_storage.save(file_name,ContentFile(f.read()))
        print "path:%s"%path
        # tmp_file=os.path.join(settings.MEDIA_ROOT,,path)
        # print "tmp_file%s"%tmp_file

        file_url_list.append(http_name+cur_date+'/'+f.name)
        # file_url_list.append(http_name+cur_date+'/'+f.name)
    report.file_path=file_url_list
    report.save()
    return HttpResponse('ok')


def admin_commit(request):
        result=cmdb_operation_records.objects.filter(run_ok=1)
        file_dict={}
        for i in result:
            # print type(i.file_path)
            l=list(eval(i.file_path))
            print l,type(l)
            file_dict[i.id]=l
        b=request.session.get('username','anybody')
        return render_to_response('admin_commit.html',{'a':result,'b':b,'file_dict':file_dict})

def sql_del(request):
        id=request.GET['id']
        cmdb_operation_records.objects.filter(id=id).delete()
        return HttpResponse("ok")

def sqlrun(request):
        a=request.GET
        id=a.items()[0][0]
        username=request.session.get('username','anybody')
        cur_date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cmdb_operation_records.objects.filter(id=id).update(run_ok=0,run_time=cur_date_time,other1=username)
        return HttpResponse("ok")

def sql_find_index(request):
        result_list=cmdb_operation_records.objects.all()

        paginator=Paginator(result_list,20)
        page=request.GET.get('page')
        try:
                contacts = paginator.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts = paginator.page(paginator.num_pages)
        return render_to_response('sql_find.html',{'contacts':contacts,'xiangmu':xiangmu})

def sql_find(request):
        a=request.GET
        print a
        auth=a['sql_auth']
        xiangmu_name=a['item']

        if auth and xiangmu_name:
                result_list=cmdb_operation_records.objects.filter(auth=auth,item=xiangmu_name)
        elif auth:
                result_list=cmdb_operation_records.objects.filter(auth=auth)
        elif xiangmu_name:
                result_list=cmdb_operation_records.objects.filter(item=xiangmu_name)
        else:
                result_list=cmdb_operation_records.objects.all()


        paginator=Paginator(result_list,20)
        page=request.GET.get('page')
        try:
                contacts = paginator.page(page)
        except PageNotAnInteger:
                contacts = paginator.page(1)
        except EmptyPage:
                contacts = paginator.page(paginator.num_pages)

        return render_to_response('sql_find.html',{'contacts':contacts,'xiangmu':xiangmu,'auth':auth})

def sql_coninfo(request):
        a=request.GET
        sql_id=a.items()[0][1]
        result=cmdb_operation_records.objects.filter(id=sql_id)
        return render_to_response('sql_coninfo.html',{'a':result,'id':sql_id})