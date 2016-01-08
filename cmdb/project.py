# -*- coding: utf-8 -*-
#coding=utf-8
__author__ = 'Ben11'
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from tools.tools import *
from tools.jenkins.jenkins_api import *
from models import *
import  jenkins
import time
from tools.get_docker_info import get_host
from views import docker_maxport
from tools.get_docker_info import docker_create
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tools.ssh_run import *
from mama100.dockerweb.models import *
soft_type=['rpc','glassfish','web','DB','nginx','lvs','redis']
# ent_type=['生产','测试','开发']
ent_type=['prd','test','dev']

#####架构名称
jg_name_object=cmdb_project_base.objects.filter(project_father=0)
jg_name=[]
for i in jg_name_object:
    jg_name.append(i.project_name)

def project_info(request):
    env='prd'
    if request.GET:
        env=request.GET['env']

        print env

        if env == 'all':
            contacts=cmdb_project.objects.all

        else:
            contacts=cmdb_project.objects.filter(ent_type=env)
    else:
        contacts=cmdb_project.objects.filter(ent_type='prd')
    return render_to_response('project_info.html', {"contacts": contacts,"env":env})

#####上线资源申请
def project_online(request):
    req_temp=request.POST
    req=dict(req_temp.iterlists())
    return render_to_response('project_online.html',{'soft_type':soft_type,'jg_name':jg_name,'ent_type':ent_type,'id':id,})

def project_online_commit(request):
    req_temp=request.POST
    print req_temp

    kaifa_man=req_temp['kaifa_man']
    jg_name=req_temp['jg_name']

    ent_type=req_temp['ent_type']
    svn=req_temp['svn']
    project_name=req_temp['project_name']
    dock_node=req_temp['dock_node']
    soft_name=req_temp['soft_name']
    soft_type=req_temp['soft_type']
    jg_name=req_temp['jg_name']
    mem=req_temp['mem']
    duankou=req_temp['duankou']
    online_time=req_temp['online_time']

    jenkins_sum(project_name,ent_type+'_'+soft_name,svn)
    ip_list=get_host(dock_node,ent_type)
    port_dict=docker_maxport()
    print "duankou============="
    print port_dict
    #build_job(ent_type+'_'+soft_name+'_build')

    ####build之后等待判断是不是产生的文件
    build_path='/var/lib/jenkins/workspace/'+ent_type+'_'+soft_name+'_build'+'/target/'
    commd='ls '+build_path
    print "build_path%s"%build_path
    file_num=run_ssh('192.168.234.17','root','root@jenkins17',commd)#####build之后路径下的文件数量
    print "file_num%s"%file_num
    while len(file_num) < 4:

        print "wait for building ......"
        print "file_num%s"%file_num
        file_num=run_ssh('192.168.234.17','root','root@jenkins17',commd)
        time.sleep(5)

    docker_create(ip_list,ent_type,soft_type,soft_name,port_dict,build_path)

    ###开始创建DEPLOY JOB
    ip_test=['192.168.234.175']###测试用生产换成ip_list
    for i in ip_list:
        duan_ip=i[8:]
        deploy_job(ent_type+'_'+soft_name,duan_ip,project_name)
####开始构建JOB
    for i in ip_list:
        duan_ip=i[8:]
        deplopy_build(ent_type+'_'+soft_name,duan_ip,project_name)
####向数据库中写入端口的信息
    for i in ip_list:
        port=port_dict[i]
        a=cmdb_docker_port(docker_ip=i,docker_port=port+'-'+str(int(port)+int(duankou)),docker_name=ent_type+soft_name)
        a.save()
    # cmdb_project.objects.filter(id=id).update(nodeip=nodeips,kaifa_man=kaifa_man,project_name=project_name,jg_name=jg_name,soft_type=soft_type,ent_type=ent_type,soft_name=soft_name)
    return HttpResponse(str(ip_list)+str(port_dict)+'<a href="http://192.168.234.139:5050/project_online"><button type="button">返回前一页</button></a>')
    # return render_to_response('project_info.html', {"contacts": contacts})

def project_online_build_job(request):
    #req_temp=request.POST
    jenkins_url = 'http://192.168.234.175:8080/login?from='
    server = jenkins.Jenkins(jenkins_url, username = 'admin', password = 'admin')
    print "will build"
    print server
    print type(server)
    server.build_job('mode-job')
    print "build end"
    # print  build_job('test_mama100_test_0221')
    # return HttpResponse("bulid 成功！！")




def project_delete(request):
    req=request.GET
    print req
    id=req['id']
    cmdb_project.objects.filter(id=id).delete()
    contacts=cmdb_project.objects.all()
    return render_to_response('project_info.html', {"contacts": contacts})

def project_create(request):
    host_all=hostpasswd.objects.all()
    ip_list=[]
    for i in host_all:
        ip_list.append(i.ip)
    jg_name=cmdb_project_base.objects.filter(project_father=0)
    return render_to_response('project_create.html',{'soft_type':soft_type,'ent_type':ent_type,'ip_list':ip_list,'jg_name':jg_name})


def project_create_commit(request):
    req_temp=request.POST
    req=dict(req_temp.iterlists())
    print req
    project_name=req_temp['project_name']
    soft_type=req_temp['soft_type']
    jg_name=req_temp['jg_name']
    online_time=req_temp['online_time']
    kaifa_man=req_temp['kaifa_man']
    soft_name=req_temp['soft_name']
    ent_type=req_temp['ent_type']
    nodeip=req['nodeip']
    nodeips=''
    for i in nodeip:
        nodeips=nodeips+i+' '
    project_father=cmdb_project_base.objects.get(project_name=jg_name).id
    cmdb_project_base.objects.create(project_name=soft_name,project_father=project_father)
    cmdb_project.objects.create(project_name=project_name,online_time=online_time,kaifa_man=kaifa_man,soft_type=soft_type,soft_name=soft_name,ent_type=ent_type,nodeip=nodeips,jg_name=jg_name)
    for ip in nodeip:
        cmdb_project_auto.objects.create(project=soft_name,ip=ip)
    # return HttpResponse("addok")
    return HttpResponse('<a href="http://192.168.234.139:5050/project_create"><button type="button">修改成功 返回前一页</button></a>')


def project_edit(request):
    host_all=hostpasswd.objects.all()
    ip_list=[]
    for i in host_all:
        ip_list.append(i.ip)
    req=request.GET
    id=req['id']
    result=cmdb_project.objects.get(id=id)
    node_ip_list=[]
    for i in result.nodeip.split():
        node_ip_list.append(i)
    #project_name=cmdb_project_base.objects.filter(project_father=0)
    return render_to_response('project_edit.html',{'result':result,'ip_list':ip_list,'soft_type':soft_type,'jg_name':jg_name,'ent_type':ent_type,'id':id,'node_ip_list':node_ip_list,})

def project_edit_commit(request):
    req_temp=request.POST
    req=dict(req_temp.iterlists())
    kaifa_man=req_temp['kaifa_man']
    jg_name=req_temp['jg_name']
    ent_type=req_temp['ent_type']
    project_name=req_temp['project_name']
    soft_name=req_temp['soft_name']
    id=req_temp['id']
    soft_type=req_temp['soft_type']
    nodeip=req['nodeip']
    nodeips=''
    for i in nodeip:
        nodeips=nodeips+i+' '

    print ent_type



    cmdb_project.objects.filter(id=id).update(nodeip=nodeips,kaifa_man=kaifa_man,project_name=project_name,jg_name=jg_name,soft_type=soft_type,ent_type=ent_type,soft_name=soft_name)
    contacts=cmdb_project.objects.all()
    return HttpResponse('<a href="http://192.168.234.139:5050/project_info"><button type="button">修改成功 返回前一页</button></a>')
    # return render_to_response('project_info.html', {"contacts": contacts})
