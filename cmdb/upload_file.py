#coding=utf-8
__author__ = 'liming'
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
def upload_file_index(request):
    soft_name=request.GET['soft_name']
    env_type=request.GET['env_type']
    viewname=request.GET['viewname']
    return render_to_response('upload_file_index.html',{'soft_name':soft_name,'env_type':env_type,'viewname':viewname})

###支持多个文件一起上传
def upload_file_commit(request):

    print "be"
    print request.FILES
    print request.POST
    print "end"
    soft_name=request.POST['soft_name']
    env_type=request.POST['env_type']
    viewname=request.POST['viewname']
    files = request.FILES.getlist('upfile')
    for f in files:
        print "%s~~~~is:~~~"%f
        file_name=os.path.join(settings.MEDIA_ROOT,soft_name,env_type,f.name)
        print file_name
        if os.access(file_name, os.F_OK):####已存在先删除
            print "cunzi"
            os.remove(file_name)
            path=default_storage.save(file_name,ContentFile(f.read()))
            os.path.join(settings.MEDIA_ROOT,path)
        else:####不存在直接上传
            print "new"
            path=default_storage.save(file_name,ContentFile(f.read()))
            print type(path)
            tmp_file=os.path.join(settings.MEDIA_ROOT,soft_name,env_type,path)
            print type(tmp_file)
    # return render_to_response('upload_file_index.html')
    # return  HttpResponse("ok")
    return HttpResponse('<a href=config_info_index?soft_name='+soft_name+'&&env_type='+env_type+'&&viewname='+viewname+'>添加成功返回</a>')