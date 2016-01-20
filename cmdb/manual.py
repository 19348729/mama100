# -*- coding: utf-8 -*-
__author__ = 'DELL'
#coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from tools.tools import *
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponse

from public.encrypt_decrypt import *
from django.contrib.auth.decorators import  *
from django.core.exceptions import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import permission_required

from tools.must_admin import *


####CONFIG INFO 配置信息
jigui_list=['A11','G2','G3','G9','G11','G12','G13']
hostsize_list=['1U','2U','4U','6U']
brand_list=['超微','IBM','DELL','其他']



################资产录入人工处理
def mannal(request):

    ip=request.GET['ip']
    brand=request.GET['brand']
    print(brand)
    online_time=request.GET['online_time']
    jigui_number=request.GET['jigui_number']
    u_size=request.GET['u_size']
    other1=request.GET['other1']

    return render_to_response('man-add.html',{'ip':ip},{'brand':brand},{'online_time':online_time},{'jigui_number':jigui_number},{'u_size':u_size},{'other1':other1})
####################### 手工 update 资产信息 ###############################
def mannal_edit(request):

    req = request.GET
    ip=req['ip']
    hostinfo=cmdb_manual_info.objects.get(ip=ip)

    return render_to_response('manual_edit.html',{'hostinfo':hostinfo,'jigui_list':jigui_list,'hostsize_list':hostsize_list,'brand_list':brand_list})
####################### 手工add 资产信息 ###############################
def manualAdd(request):
        b={}
        b = request.POST
        print b
        ip=b['ip']
        brand=b['brand']
        online_time=b['onload_time']
        u_size=b['u_size']
        jigui_number=b['jigui_number']
        other1=b['other1']
        cmdb_manual_info.objects.filter(ip=ip).update(online_time=online_time,u_size=u_size,brand=brand,jigui_number=jigui_number,other1=other1)
        # cmdb_manual_info.objects.filter(ip=ip).delete()
        # fb=cmdb_manual_info(ip=ip,brand=brand,online_time=online_time,u_size=u_size,jigui_number=jigui_number)
        # fb.save()

        return HttpResponse('<a href="/manual_index"><button type="button">修改成功 返回前一页</button></a>')

#def manual_zichan(request):
 #       result=cmdb_manual_info.objects.all()
 #       return render_to_response('manual_zichan.html',{'cons':result})
@must_admin
def manual_index(request):
################先从自动表中取出所有的我物理主机存入到手工表中
    wu_host=cmdb_auto_info.objects.filter(vorw='物理机')
    wuip_list=[]
    wuip2_list=[]
    for i in wu_host:  ####取出自动发现表中的所有物理主机的IP，存入到wuip_list列表中
        wuip_list.append(i.ip)
    try:  ####取出手工表中的所有主机的IP，存入到wuip2_list列表中
        cons = cmdb_manual_info.objects.all()

        for j in cons:
            wuip2_list.append(j.ip)
    except:
           pass
    for i in wuip_list:########现从个列表进行比较，少的就生成一个对像存放表中
        if i in wuip2_list:
            pass
        else:
            print i
            new_info=cmdb_manual_info(ip=i)
            new_info.save()
    cons = cmdb_manual_info.objects.all()
    return render_to_response('manual_zichan_index.html', {"contacts": cons})

########################密码管理
a=EncryptDecrypt()
key=138

def hostpasswd_index(request):
        return render_to_response('hostpasswd_index.html')


def hostpasswd_find(request):
        b=request.POST
        if b['ip']:
                ip=b['ip']
                try:
                        jieguo=hostpasswd.objects.filter(ip__contains=ip)
                except ObjectDoesNotExist:
                        return HttpResponse("no this IP")

                c={}
                sum_dict={}
                xlie=1
                for i in jieguo:

                    c['ip']=i.ip
                    c['username']=i.username
                    c['password']=a.decrypt(key,i.password)
                    sum_dict[xlie]=c
                    c={}
                    xlie=xlie+1
        else: sum_dict={}
        return render_to_response('hostpasswd_index.html',{'jieguo':sum_dict})


    #paginator = Paginator(sum_dict,10) # Show 25 contacts per page
    #
    # page = request.GET.get('page')
    # try:
    #     contacts = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     contacts = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     contacts = paginator.page(paginator.num_pages)
    #
    # return render_to_response('hostpasswd_index.html', {"jieguo": contacts})

def hostpasswd_add(request):
        ip=request.POST['ip']
        username=request.POST['username']
        password=request.POST['password']
        en_password=a.encrypt(key,password)
        result=hostpasswd.objects.filter(ip=ip,username=username)
        if result:
                hostpasswd.objects.filter(ip=ip,username=username).update(password=en_password)
                return HttpResponse("password update success")
        else:
                hostpasswd.objects.create(ip=ip,username=username,password=en_password)
                return HttpResponse("password add success")