#!/usr/bin/python

from mysql_run import *
from encrypt import *
key=138
def encrypt_password():
	iplist = open("/mama100/mama100/tools/test115.txt",'rb')
	#conn_mysql('delete from hostpasswd')
	for line in iplist:
		#print line.split(' ')
		list=line.split()
		ip=list[0]
		username=list[1]
		password=list[2]
		en_password=encrypt(key,password)
		print password
		#print list[2],len(list[2])

		sql='insert into  hostpasswd(ip,username,password) values (\''+ip+'\',\''+username+'\',"'+en_password+'")'
		#print sql
		conn_mysql(sql)
	iplist.close()

def decrypt_password(ip):
	sql='select password from hostpasswd where ip="'+ip+'"'
	tm_password=conn_mysql(sql)
	if tm_password:
		en_password=tm_password[0][0]
		password=decrypt(key,en_password)
		return password
	else:
		password=''
		return password


if __name__=="__main__":
	encrypt_password()
	#print decrypt_password('192.168.234.12')
