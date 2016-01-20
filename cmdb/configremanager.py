#coding=utf-8
__author__ = 'Ben'
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tools.getdir import *
from tools.ssh_run import *
from models import *
import time
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tools.zabbix.sum_result import *
import jenkins


currentdate=time.strftime("%Y-%m-%d", time.localtime())
config_bak_folder='/config_bak/'
#def hostinfo_index(request):
#    result=cmdb_auto_info.objects.all()
#    return render_to_response('hostinfo_index.html',{'cons':result})


####把一个列表转化成为一个字典
def change_list_dict(list_a):
        dict_a={}
        for i in list_a:
                b=i.split()
                for j in b:
                        dict_a[b[1]]=b[0]
        return dict_a

####把两个字典合并，KEY取唯一

def add_dict(a,b):
        sum_dict={}
        for k,v in a.items():
                sum_dict[k]=v
                if b[k] not in v:

                        sum_dict[k]=sum_dict[k]+','+b[k]
                        #sum_dict[k].append(b[k])
        return sum_dict



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

def mkdir_fodel(title):
    path = "/mama100/jenkins/deploy/patch"
    title = "title"
    new_path = os.path.join(path, title)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    return HttpResponse("create succsse")

def config_info_commit(request):
    req=request.POST
    print req
    file_name=req['file_name']
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
#####编辑配置文件
def config_edit(request):
    req=request.GET
    file_name=req['file_name']
    return render_to_response('config_edit.html',{'file_name':file_name})

####删除一个配置文件
def config_delte(request):
    print "wokdo"
    req=request.GET
    file_name=req['file_name']
    soft_name=request.GET['soft_name']
    env_type=request.GET['env_type']
    viewname=request.GET['viewname']
    try:
        os.remove(file_name)
        return HttpResponse('<a href=config_info_index?soft_name='+soft_name+'&&env_type='+env_type+'&&viewname='+viewname+'>删除成功返回</a>')
    except:
        return HttpResponse('<a href=config_info_index?soft_name='+soft_name+'&&env_type='+env_type+'&&viewname='+viewname+'>删除失败返回</a>')

# def config_edit_old(request):
#     req=request.GET
#     print "#########%s#######"%req
#     soft_name=req['soft_name']
#     try:
#         base_dir='/mama100/jenkins/deploy/patch/'
#         find_dir=base_dir+soft_name
#         find_dir_list=get_dir_file(find_dir)
#         print find_dir_list
#         if find_dir_list:
#             return render_to_response('config_edit.html',{'find_dir_list':find_dir_list})
#         else:
#             return HttpResponse("没有配置文件")
#     except OSError:
#         return HttpResponse("没有此目录,请增加")

####提供ip ,文件路径，返回一个字典 eg. {filename:[ip,md5]




def config_info_index(request):
    soft_name=request.GET['soft_name']
    ###取出精确的软件名称
    jing1=soft_name.replace('prd_','')
    jing2=jing1.replace('prd-','')
    jing3=jing2.replace('pre_','')
    jing4=jing3.replace('prd-','')
    env_type=request.GET['env_type']
    viewname=request.GET['viewname']
    jenkins_url = 'http://192.168.234.17:8083/view/'+viewname
    server = jenkins.Jenkins(jenkins_url, username = 'admin', password = '20151019mama100')

    ###取IP，配置文件名，和目录
    file_object=cmdb_project.objects.get(soft_name=soft_name,ent_type=env_type)
    # print file_object
    # print type(file_object)
    iplist=file_object.nodeip.split()
    print iplist
    base_path=file_object.other2


    try:
        tmp_list=server.get_jobs()
    except:
        return HttpResponse("没有视图，请添加")

    # print "tmp_list is %s~~~"%tmp_list
    job_name_list=[]
    for i in tmp_list:
        job_name_list.append(i['fullname'])
    try:
        base_dir='/mama100/jenkins/deploy/patch/'
        find_dir=base_dir+soft_name+'/'+env_type
        print "find:%s"%find_dir
        find_dir_list=get_dir_file(find_dir)###取出所有的配置文件名
        print find_dir_list
        file_name_list=''####把需要查找的文件名加上应用的目录路径组合
        for i in find_dir_list:
            file_name_list=file_name_list+base_path+os.path.basename(i)+' '
		

        ####开始比较配置文件与各服务器的MD5值
        md5_dict={}
        list_a=[]
        error_dict={}
        for ip in iplist:
            password=get_password(ip)
            commd='md5sum '+file_name_list	
            print commd
            result=run_ssh(ip,'root',password,commd).split('\n')
            print "reult=%s"%result
            if result==['']:
                error_dict[ip]=file_name_list
            else:
                list_a.append(change_list_dict(result))
        #print list_a
        #print "==="*12
        #print error_dict
        #print 'md5sum '+find_dir+'/*'
        bendi=os.popen('md5sum '+find_dir+'/*').read()
        bendi_dict=change_list_dict(bendi.split('\n'))
        
        ###需要把本地的文件绝对路径转化为虚假的应用服务器上的目录结构
        bendi_temp_dict={}
        for k,v in bendi_dict.items():
            f_name1=os.path.basename(k)
            f_name2=os.path.join(base_path,f_name1)
            bendi_temp_dict[f_name2]=v


        print 'bendkkk'
        print bendi_temp_dict
        list_a.append(bendi_temp_dict)####最后把本地的MD5验证结果加入到列表中
        md5_dict=reduce(add_dict,list_a)
        print 'ni hao nb'
        print md5_dict
        ####最后最后把应用的目录转化成为只有文件名的字典
        end_md5_dict={}
        for k,v in md5_dict.items():
            f_name1=os.path.basename(k)
            end_md5_dict[f_name1]=v

        return render_to_response('config_info_index.html',{'find_dir_list':find_dir_list,'env_type':env_type,'soft_name':soft_name,'job_name_list':job_name_list,'viewname':viewname,'md5_dict':end_md5_dict,'error_dict':error_dict})

    except OSError:
        return HttpResponse("没有此目录,请增加")








