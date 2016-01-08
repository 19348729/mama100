#!/usr/local/bin/python
# -*- encoding:utf8 -*-
import  jenkins
import re
def get_server_instance():
    jenkins_url = 'http://192.168.234.21:8083/'
    #jenkins_url = 'http://192.168.234.21:8083/login?from='
    server = jenkins.Jenkins(jenkins_url, username = 'admin', password = 'jenkins1234')
    return server

def create_jenkins_views():
	server.create_view('EMPTY', jenkins.EMPTY_VIEW_CONFIG_XML)
	view_config = server.get_view_config('EMPTY')
	views = server.get_views()
	server.delete_view('EMPTY')


def get_job_details(xmname):
    # Refer Example #1 for definition of function 'get_server_instance'
    # server = get_server_instance()
	
    f=open('/tmp/config.xml','rb')
    b=f.read()
    pattern=re.compile(r'svn:.<')
    print re.search(pattern,b).group()
	#server.reconfig_job('nihennb',b)
	#print "sdfj"
	#a=server.get_job_config('nihennb')
	#print a
	
	
	#server.copy_job('mode-job',xmname)
	#print server.get_jobs_info('nihennb')
    #for j in server.get_jobs():
    #    job_instance = server.get_job(j[0])
        #print 'Job Name:%s' %(job_instance.name)
        #print 'Job Description:%s' %(job_instance.get_description())
    #    print 'Is Job running:%s' %(job_instance.is_running())
        #print 'Is Job enabled:%s' %(job_instance.is_enabled())

get_job_details('nihennb1')	
