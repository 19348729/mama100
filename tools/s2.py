#!/usr/bin/python
#-*- coding: UTF-8 -*-
###by liming
###this file to multiprocessing run ssh command


import paramiko
import pexpect
#from ssh_know import *

class ssh_know:
    def fun_ssh(self,ip,username):		
        a='ssh '+username+'@'
        cmd=a+str(ip)
        child = pexpect.spawn(cmd)
        index = child.expect(['connecting','password',pexpect.EOF,pexpect.TIMEOUT],timeout=-1)
        if index == 0:
            child.sendline('yes\n')

class runssh_host:
    def run_commd(hostname,username,password,commd):
#####在一台主机上执行命令
        ssh=paramiko.SSHClient()
        known_hosts='/root/.ssh/known_hosts'
        try:
            ssh.load_system_host_keys(known_hosts)
        except IOError:
            print "no known_hosts file"
        try:
            ssh.connect(hostname=hostname,username=username,password=password)
        except paramiko.SSHException:
            print "%s is not in known_hosts" %hostname
            p=ssh_know()
            p.fun_ssh(hostname,username)
            ssh.load_system_host_keys(known_hosts)
            ssh.connect(hostname=hostname,username=username,password=password)
            stdin,stdout,stderr=ssh.exec_command(commd)
            print stdout.read()
            return stdout.read()
        else:
            stdin,stdout,stderr=ssh.exec_command(commd)
            print stdout.read()
            return stdout.read()


if __name__=="__main__":
	run_commd('192.168.233.2','root','root1234','uptime')
