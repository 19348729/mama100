#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import *
# Create your views here.
from public.encrypt_decrypt import *
from django.contrib.auth.decorators import  *
from django.core.exceptions import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import *
from tools.auth_test import *
from tools.must_admin import *
import paramiko
import threading
import logging
from urllib import unquote

logfile='change_password.log'

a=EncryptDecrypt()
key=138

####获取所有主机IP列表
ip_all=hostpasswd.objects.all()
ip_all_list=[]
for i in ip_all:
    ip_all_list.append(i.ip)



####多线程函数
def run_threading(list_host):
    for i in list_host:
        print "begin"
        print i,type(i)
        p=threading.Thread(target=change_password,args=(i))
        p.start()
        # p.join()

####修改密码函数
def change_password(ip,username,cur_pass,new_pass,port=22):
    # ip=list_a[0]
    # username=list_a[1]
    # cur_pass=list_a[2]
    # new_pass=list_a[3]
    logging.basicConfig(level=logging.INFO,filename=logfile)
    s=paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(ip,port,username,cur_pass)
    # commd='ifconfig'
    commd='echo %s|passwd --stdin %s'%(new_pass,username)
    stdin,stdout,sterr=s.exec_command(commd)
    print 'commd:'+commd
    out_resutl=stdout.read()
    print out_resutl
    logging.info(ip+':'+commd+out_resutl)
    s.close()
    result=auth_test(username,ip,new_pass)
    if result:
        en_password=a.encrypt(key,new_pass)
        hostpasswd.objects.filter(ip=ip,username=username).update(password=en_password)
    else:
        logging.info(ip+':'+username+':'+cur_pass+"change error")
    return result


@must_admin
def hostpasswd_index(request):
    return render_to_response('hostpasswd_index.html',{'ip_all_list':ip_all_list})

@must_admin
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
        return render_to_response('hostpasswd_index.html',{'jieguo':sum_dict,'ip_all_list':ip_all_list})

def hostpasswd_add(request):
    ip=request.POST['ip']
    username=request.POST['username']
    password=request.POST['password']
    print ip,username,password
    if ip == '' or username == '' or password == '':
        return HttpResponse("must input:ip,username,password")
    en_password=a.encrypt(key,password)
    if request.POST.has_key('online'):
        online_changehost=True####此处增加了一个标记位，在前端做一个标记，询问是不是在线修改服务器的密码选项
    else:
        online_changehost=False

#####能找到学，再然后密码更新成功，才去修改数据库的密码信息,以下逻辑是现有的密码是正确的，才可以修改
#####并不是数据库存的密码是错误的，然后在这里修改
    results=hostpasswd.objects.filter(ip=ip,username=username)
    if results:
        if online_changehost:
            cur_pass=a.decrypt(key,hostpasswd.objects.get(ip=ip,username=username).password)
            if change_password(ip,username,cur_pass,password,port=22):
                hostpasswd.objects.filter(ip=ip,username=username).update(password=en_password)
        else:
            hostpasswd.objects.filter(ip=ip,username=username).update(password=en_password)

        return HttpResponse("password update success")
    else:
        hostpasswd.objects.create(ip=ip,username=username,password=en_password)
        return HttpResponse("password add success")


def hostpasswd_auth(request):
    req=request.GET
##############此处处理了前端的密码字符会传入特殊字符情况，前端传入以下样式
##########<QueryDict: {u'ip=192.168.234.65&username=glassfish&password=hsymama100!#$': [u'']}>
    list_temp=req.keys()[0].split('&')
    dict_temp={}
    for i in list_temp:
        num=i.find('=')
        dict_temp[i[:num]]=i[num+1:]
##########处理得到dict_temp字典
    hostname=dict_temp['ip']
    username=dict_temp['username']
    password=dict_temp['password']
    print username,hostname,password
    result=auth_test(username,hostname,password)
    return HttpResponse(result)

###批量处理
def batch_change_passwd(request):
    req_temp=request.POST
    req=dict(req_temp.iterlists())
    # print req
    username=req_temp['username']
    password=req_temp['password']
    if username == '' or password == '':
        return HttpResponse("must input:username,password")
    iplist=req['iplist']
    # print username,password
    # print iplist
    sum_list=[]
    temp_list=[]
    for i in iplist:
        cur_pass_encrypt=hostpasswd.objects.get(ip=i,username=username).password
        cur_pass=a.decrypt(key,cur_pass_encrypt)
        temp_list=[i,username,cur_pass,password]
        sum_list.append(temp_list)
    # print sum_list
    run_threading(sum_list)
    return render_to_response('hostpasswd_index.html')


#####用户修改密码
def change_password_index(request,username):
    print username
    return render_to_response('update_passwd.html',{'username':username})

