#coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from tools.tools import *
from models import *
from mama100.dockerweb.models import *


from django.http import HttpResponse

# 引入我们创建的表单类
from .forms import AddForm

def index(req):
    return render_to_response('index.html')

##用户登录页面
def login_index(request):
    return render_to_response('login.html')

###只是验证用户和密码，返回TRUE/FALSE
def login_check_only(request):
    a=request.POST
    username=a['username']
    password=a['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            return  HttpResponse("ok")
        else:
            return  HttpResponse("not")
    else:
        return  HttpResponse("not")

#######修改密码
def change_password_commit(request):
    a=request.POST
    username=a['username']
    oldpass=a['oldpass']
    newpass=a['newpass']
    user = authenticate(username=username, password=oldpass)
    print username,oldpass,newpass,user
    print "change_password_commit"
    user.set_password(newpass)
    user.save()
    return  HttpResponse("ok")

##用户登录验证
def login_check(request):
    a=request.POST
    username=a['username']
    password=a['password']

    user = authenticate(username=username, password=password)

    request.session['username']=username
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('index.html',{'username':username})
            # Redirect to a success page.
        else:
            return HttpResponse("用户状态异常")
            # Return a 'disabled account' error message
    else:
        return HttpResponse("用户名或密码错误")
        # Return an 'invalid login' error message
###用户退出
def user_logout(request):
#       del request.session['username']
        logout(request)
        return render_to_response('login.html')

###控制台展示
def control_index(request):
    v=cmdb_auto_info.objects.filter(vorw='虚拟机')
    w=cmdb_auto_info.objects.filter(vorw='物理机')
    vhost=len(v)
    whost=len(w)
    return render_to_response('control.html',{'vhost':vhost,'whost':whost})

def docker_maxport():
    contacts=cmdb_docker_port.objects.all()
    port_dict={}
    port_temp_dict={}
    for i in contacts:
       if port_temp_dict.has_key(i.docker_ip):
            port_temp_dict[i.docker_ip]=port_temp_dict[i.docker_ip]+'-'+i.docker_port
       else:
           port_temp_dict[i.docker_ip]=i.docker_port

    for ip,port in port_temp_dict.items():
        maxport=max(port.split('-'))
        port_dict[ip]=maxport

    return port_dict

def form(request):
    if request.method == 'POST':# 当提交表单时

        form = AddForm(request.POST) # form 包含提交的数据

        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:# 当正常访问时
        form = AddForm()
    return render(request, 'form.html', {'form': form})

