#!/usr/local/bin/python
#*- coding: UTF-8 -*-
from  multiprocessing import Process
#from  mysql_run import *
from mysql_run import *

from password_mysql import *
import paramiko
import os
import pexpect
from encrypt import *


##遇到第一次连接的主机时去掉ssh的yes提示
def del_yes(ip):
	cmd="ssh root@"+ip
	child = pexpect.spawn(cmd)
  	index = child.expect(['connecting','password',pexpect.EOF,pexpect.TIMEOUT],timeout=-1)
	if index == 0:
		child.sendline('yes\n')

###真正去ssh服务器执行脚本返回执行结果
def run_ssh(ip,username,password,cmd):
    #print "wokao:"
    #print ip,username,password,cmd
    try:
        ssh=paramiko.SSHClient()
        known_hosts='/root/.ssh/known_hosts'
        ssh.load_system_host_keys(known_hosts)
        ssh.connect(hostname=ip,username=username,password=password)
        stdin,stdout,stderr=ssh.exec_command(cmd)
        a=stdout.read().rstrip()
        #a=stdout.read().split('\n')
        #print "nb====%s"%a
        return a
    except Exception,e:
        print e
        return False


###从数据库取出所有的密码和IP对应关系，返回一个字典
def get_all_password():
    sum_dict={}
    sql='select ip,username,password from hostpasswd'
    temp_result=conn_mysql(sql)
    for i in temp_result:
        temp_password={}
        # print i
        temp_password[i[1]]=i[2]
        if sum_dict.has_key(i[0]):
            sum_dict[i[0]].append(temp_password)
        else:
            sum_dict[i[0]]=[temp_password]
    return sum_dict

##### 给我IP，我给你密码
def get_password(ip,username='root'):
    password_all={}
    password_all=get_all_password()
    tmp_pass=password_all[ip]
    # print tmp_pass
    for i in tmp_pass:
        # print str(i.keys()[0]),str(username)
        #
        # print str(i.keys())==str(username)
        if i.keys()[0] == username:
            result=decrypt(138,i[username])
    # print result
    return result

