#coding=utf-8

from django.shortcuts import render

# Create your views here.
import docker
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import *
from django.core.exceptions import ObjectDoesNotExist
from django import forms
####page 
from django.core.paginator import *


#
# c=docker.Client(base_url='tcp://192.168.115.31:2375',version='1.17',timeout=10)
# c2=docker.Client(base_url='tcp://192.168.234.20:2375',version='1.17',timeout=10)
# c4=docker.Client(base_url='tcp://192.168.233.2:2375',version='1.17',timeout=10)
#
#
#
# image1=c.images()
# image2=c2.images()
# image4=c4.images()
#
docker_ip = ['192.168.115.31', '192.168.234.20','192.168.233.2']
# #【容器创建】使用
# docker_ip_image={'192.168.115.31':image1, '192.168.234.20':image2,  '192.168.233.2':image4}




#镜像管理
#@admin_check
def docker_images_index(request):
	#获取docker服务器IP
	if request.POST.has_key('ip_select'):
		docker_server_ip = request.POST.get('ip_select')
	else:
		docker_server_ip = '192.168.115.31'
	
	docker_url = "tcp://%s:2375" %(docker_server_ip)
	docker_client=docker.Client(base_url=docker_url,version='1.17',timeout=10)

	img_list1=docker_client.images()
	#selected_docker_ip		被选中的docker服务器IP
	return render_to_response('Image_index.html',{'imgs':img_list1, 'docker_ip':docker_ip, 'selected_docker_ip':docker_server_ip})

def del_img(request):
	if request.GET.has_key('ip_select'):
		docker_server_ip=request.POST['ip_select']
	else:
		docker_server_ip = '192.168.115.31'

	docker_url = "tcp://%s:2375" %(docker_server_ip)
	c=docker.Client(base_url=docker_url,version='1.17',timeout=10)

	a=str(request.GET.keys())[3:-2]
	c.remove_image(a)
	return HttpResponse(a)


def docker_con_index(request):
    dockerport_info=docker_port(request)
    print type(dockerport_info)
    for k,v in dockerport_info.items():
        print k,v
    if request.POST.has_key('ip_select'):
        docker_server_ip=request.POST['ip_select']
    else:
        docker_server_ip = '192.168.115.31'

    docker_url = "tcp://%s:2375" %(docker_server_ip)
    docker_client=docker.Client(base_url=docker_url,version='1.17',timeout=10)

    con_list=docker_client.containers(all=True)
    print con_list
    port_dict={}
    port_list=[]
    print "wokkkkkkkk"
    for i in con_list:
            ports=i.get('Ports')
            prot_list=[]
            for j in ports:
                    port_list=[]
                    port_list.append("%s:%s"%(j.get('PublicPort'),j.get('PrivatePort')))
            #con_port=con_list[0]['Ports']
            port_dict[i.get('Id')]=port_list

    #selected_docker_ip     被选中的docker服务器IP
    return render_to_response('ConManager_index.html',{'cons':con_list,'port_dict':port_dict, 'docker_ip':docker_ip, 'selected_docker_ip':docker_server_ip,'dockerport_info':dockerport_info})


def constopstart(request):
	print "haha ..........."
	print request.GET
	if request.GET.has_key('docker_server_ip'):
		docker_server_ip=request.GET['docker_server_ip']
	else:
		docker_server_ip = '192.168.115.31'
	print docker_server_ip
	docker_url = "tcp://%s:2375" %(docker_server_ip)
	c=docker.Client(base_url=docker_url,version='1.17',timeout=10)
	for a in request.GET.keys():
		print "nbbbnnnnbb"
		print a

        if request[a] == 'stop' or request[a]== 'start':
			b=request.GET[a]
			print b
			if 'stop' in b:
				print '*********************************'
				c.stop(container=a)
			elif 'start' in b:
				c.start(container=a)
			else:
				c.remove_container(container=a)
	return render_to_response('constopstart.html',{'b':b})



def ConCreate(request):
    c=docker.Client(base_url='tcp://192.168.115.31:2375',version='1.17',timeout=10)
    c2=docker.Client(base_url='tcp://192.168.234.20:2375',version='1.17',timeout=10)
    c4=docker.Client(base_url='tcp://192.168.233.2:2375',version='1.17',timeout=10)



    image1=c.images()
    image2=c2.images()
    image4=c4.images()

    docker_ip = ['192.168.115.31', '192.168.234.20','192.168.233.2']
    #【容器创建】使用
    docker_ip_image={'192.168.115.31':image1, '192.168.234.20':image2,  '192.168.233.2':image4}

    img_list=c.images()
    docker_image=[image1, image2]
    return render_to_response('ConCreate.html',{'docker_ip_image':docker_ip_image})



def Conadd(request):
	print request.GET
	
	img_name=str(request.GET['sel'][3:-2])
	phy_dir=request.GET['phy_dir'].split(',')
	con_dir=request.GET['con_dir'].split(',')
	phy_port=request.GET['phy_port'].split(',')
	con_port=request.GET['con_port'].split(',')
	con_commd=request.GET['con_commd']
	con_name=request.GET['con_name']
	cpu_name=request.GET['cpu_name']
	mem_name=request.GET['mem_name']
	print img_name
	print len(img_name)
    # print type(img_name)
	
	i=0
	j=0
	dic_dir={}
	dic_port={}
	while i<len(phy_port):
			dic_port[con_port[i]]=phy_port[i]
			i=i+1
	while j<len(phy_dir):
			dic_dir[phy_dir[j]]=con_dir[j]
			j=j+1
	print "begin...."	
	print con_dir,
	
	print "begin...."	
	#container=c.create_container(image='redis3.0:latest',name=con_name,command=con_commd,ports=con_port,volumes=con_dir,host_config=docker.utils.create_host_config(binds=dic_dir,port_bindings=dic_port))
	container=c.create_container(image=img_name,name=con_name,command=con_commd,ports=con_port,host_config=docker.utils.create_host_config(binds=dic_dir,port_bindings=dic_port))
	#container=c.create_container(image='redis3.0:latest',command='/bin/sleep 20')
	c.start(container=container.get('Id'))
	return render_to_response('Conadd.html',{'img_name':img_name,'phy_dir':phy_dir,'con_dir':con_dir,'phy_port':phy_port,'con_port':con_port,'con_commd':con_commd,'con_name':con_name,'dic_dir':dic_dir,'dic_port':dic_port})


def docker_port(request):
    contacts=cmdb_docker_port.objects.all()
    docker_dit={}
    for j in contacts:
        docker_dit[j.docker_name]=j.docker_port
    return docker_dit
    #return render_to_response('docker_port.html', {"contacts": contacts,"docker_dit":docker_dit})


    # return HttpResponse("OK")

# from django.shortcuts import render
# from django.http import HttpResponse

# 引入我们创建的表单类
