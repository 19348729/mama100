# -*- coding: utf-8 -*-
#!/usr/local/bin/python
import  jenkins
import re
import time


####取Jenkins对像
def get_server_instance():
    jenkins_url = 'http://192.168.234.17:8083/login?from='
    server = jenkins.Jenkins(jenkins_url, username = 'admin', password = '20151019mama100')
    return server


###创建一个新的VIEWS
def create_jenkins_views(view_name):
    server = get_server_instance()
    server.create_view(view_name,jenkins.EMPTY_VIEW_CONFIG_XML)
    view_config = server.get_view_config(view_name)
    #print view_config

####修改views的config,从而实现添加JOB到view中

def change_view_config(view_name,new_job=''):
    server = get_server_instance()
    new_config=''
    print "xiugai view add job into"
    print view_name,new_job
    old_config=server.get_view_config(view_name)
    for i in old_config.split('\n'):
        new_config=new_config+i+'\n'
        if 'comparator' in i:
            new_config=new_config+'    <string>'+new_job+'</string>'+'\n'
    server.reconfig_view(view_name,new_config)
    #print server.get_view_config(view_name)





####从mode-job模板COPY出一个新的JOB
def create_jenkins_job(job_name,type,ip=''):

    if type=='build':
        modesss='mode-job'
        job_name=job_name+'_'+type
    else:
        modesss='mode-deploy'
        job_name=job_name+'_docker_'+ip+'_'+type
    server = get_server_instance()
    print modesss,job_name
    server.copy_job(modesss,job_name)
    job_config=server.get_job_config(job_name)
    #print job_config



###修改JOB的config,使其立即生效
def change_job_config(job_name,new_svn=''):
    print "change job config %s"%job_name
    server = get_server_instance()
    job_config=server.get_job_config(job_name)
    pattern=re.compile(r'<remote>\S*</remote>')
    new_config=re.sub(pattern,'<remote>'+new_svn+'</remote>',job_config)
    server.reconfig_job(job_name,new_config)
    job_config=server.get_job_config(job_name)
    server.disable_job(job_name)
    server.enable_job(job_name)
    #print job_config

    ###修改deploy JOB的config,使其立即生效
def change_deployjob_config(job_name,ipaddress):
    soft_name=job_name
    ip='192.168.'+ipaddress
    job_name=job_name+'_docker_'+ipaddress+'_deploy'
    print "begin to change deploy job config %s"%job_name
    server = get_server_instance()
    job_config=server.get_job_config(job_name)
    pattern=re.compile(r'soft_name')
    new_config=re.sub(pattern,soft_name,job_config)###替换软件名
    pattern=re.compile(r'ipaddress')
    new_config2=re.sub(pattern,ip,new_config )  ##替换IP地址
    server.reconfig_job(job_name,new_config2)
    job_config=server.get_job_config(job_name)
    server.disable_job(job_name)
    server.enable_job(job_name)
    print "xiu gai hou de :"
    #print job_config

###build a job
def build_job(job_name):
    server = get_server_instance()
    time.sleep(5)
    print "i will build"
    print job_name,server
    server.build_job(job_name)
    print "i build end"
    time.sleep(5)
    print "build job %s ing.........."%(job_name)

def deplopy_build(job_name,ipaddress,viewnam):
    job_name=job_name+'_docker_'+ipaddress+'_deploy'
    print "deploy beging........%s"%job_name
    server = get_server_instance()
    server.build_job(job_name)
    print "deploy job ............"


#####create a deploy job
def deploy_job(job_name,ipaddress,viewname):
    print "deploy job name is %s"%job_name
    create_jenkins_job(job_name,'deploy',ipaddress)
    change_deployjob_config(job_name,ipaddress)
    change_view_config(viewname,job_name)

def jenkins_sum(view_name,job_name,new_svn):
    print view_name,job_name,new_svn
    server = get_server_instance()
    print "hahahahah"
    create_jenkins_views(view_name)
    print "##############create view##############"
    create_jenkins_job(job_name,'build')
    print "##############create job###############"
    change_job_config(job_name+'_build',new_svn)
    change_view_config(view_name,job_name+'_build')
    print "##############build job################"






#create_jenkins_views('view_test')
#create_jenkins_job('job_test')
#change_job_config('job_test','svn://abc.com/testalsdjf')
#change_view_config('view_test','job_test')
#server = get_server_instance()
#server.build_job('test12212')
