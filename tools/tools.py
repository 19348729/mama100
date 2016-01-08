#!/usr/local/bin/python
# -*- encoding:utf8 -*-
__author__ = 'Ben'
import MySQLdb
import paramiko
import pexpect
class mysql_public_tools:
	def __init__(self):
		self.DB_HOST = '127.0.0.1'
		self.DB_PORT = 3306
		self.DB_USER = 'root'
		self.DB_PWD = ''
		self.DB_NAME = 'mama100'
		self.conn = self.getConnection()
	def getConnection(self):
		return MySQLdb.Connect(
			host=self.DB_HOST, #设置MYSQL地址
			port=self.DB_PORT, #设置端口号
			user=self.DB_USER, #设置用户名
			passwd=self.DB_PWD, #设置密码
			db=self.DB_NAME, #数据库名
			charset='utf8' #设置编码
                           )

	def query(self, sqlString):
		cursor=self.conn.cursor()
		cursor.execute(sqlString)
		returnData=cursor.fetchall()
		cursor.close()
		self.conn.close()
		return returnData

	def update(self, sqlString):
		cursor=self.conn.cursor()
		cursor.execute(sqlString)
		self.conn.commit()
		cursor.close()
		self.conn.close()
class ssh_know:
    def fun_ssh(self,ip,username):
        a='ssh '+username+'@'
        cmd=a+str(ip)
        child = pexpect.spawn(cmd)
        index = child.expect(['connecting','password',pexpect.EOF,pexpect.TIMEOUT],timeout=-1)
        if index == 0:
		    child.sendline('yes\n')

class runssh_host:
    def run_commd(self,hostname,username,password,commd):
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
    k=runssh_host()
    k.run_commd('192.168.233.2','root','root1234','uptime')
