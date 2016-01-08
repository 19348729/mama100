# -*- coding: utf-8 -*-
#coding=utf-8
__author__ = 'NICK'
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from tools.tools import *
from tools.jenkins.jenkins_api import *
from models import *
import time
from tools.get_docker_info import get_host
from views import docker_maxport
from tools.get_docker_info import docker_create
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tools.ssh_run import *
from mama100.dockerweb.models import *
type=['故障','变更','all']
# ent_type=['生产','测试','开发']
type_level=['特大','重大','较大','一般']


def records(request):
    type='故障'
    if request.GET:
        type=request.GET['type']
        print type
        if type == 'all':
            contacts=cmdb_operation_records.objects.all
        else:
            contacts=cmdb_operation_records.objects.filter(type=type)
    else:
        contacts=cmdb_operation_records.objects.filter(type='故障')
    return render_to_response('records.html', {"contacts": contacts,"type":type})