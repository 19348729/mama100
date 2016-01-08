#!/usr/local/bin/python
#*- coding: UTF-8 -*-
from  multiprocessing import Process
#from  mysql_run import *
from mysql_run import *
import string

def kvm(vorw):
	sql='select ip,mac from cmdb_auto_info where vorw ="'+vorw+'"'
	a=conn_mysql(sql)
	b={}
	for i in a:
		k=list(i)
		b[k[0]]=k[1:]
	return b
mac_wu=kvm("物理机")
mac_v=kvm("虚拟机")


def mactoip(value):
	global mac_wu
	for k,v in mac_wu.items():
		if value.upper() in str(v):
			return k
#print mactoip('54:00:53:50:c7')

for k,v in mac_v.items():
	p_ip=mactoip(v[0])
	print k,p_ip,
	sql='update cmdb_auto_info set parent_ip="'+p_ip+'" where ip="'+k+'"' 
	print sql
	conn_mysql(sql)
