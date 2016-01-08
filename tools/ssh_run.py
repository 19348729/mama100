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
	try:
		ssh=paramiko.SSHClient()
		known_hosts='/root/.ssh/known_hosts'
		ssh.load_system_host_keys(known_hosts)
		ssh.connect(hostname=ip,username=username,password=password)
		stdin,stdout,stderr=ssh.exec_command(cmd)
		a=stdout.read().split('\n')
		return a
	except:
		return False


###从数据库取出所有的密码和IP对应关系，返回一个字典
def get_all_password():
	temp_password={}
	sql='select ip,password from hostpasswd'
	temp_result=conn_mysql(sql)
	for i in temp_result:
		temp_password[i[0]]=i[1]
	return temp_password

##### 给我IP，我给你密码
def get_password(ip):
    password_all={}
    password_all=get_all_password()
    single_password=decrypt(138,password_all[ip])
    return single_password

