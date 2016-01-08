#!/usr/bin/env python2.7

#coding=utf-8
import json
import urllib2
from auth import *

url1 = "http://192.168.234.84/zabbix/api_jsonrpc.php"

header = {"Content-Type":"application/json"}

auth_id=get_auth_id()
def get_items_id(hostid):
	data = json.dumps(

	{

	   "jsonrpc":"2.0",

	   "method":"item.get",

	   "params":{

		   "output":["itemids","key_"],
			"hostids":hostid,
	   },

	   "auth":auth_id,

	   "id":1,

	})


	request = urllib2.Request(url1,data)

	for key in header:
		request.add_header(key,header[key])


	result = urllib2.urlopen(request)

	response = json.loads(result.read())

	result.close()
	###return resutl list 
	bzlist=['system.cpu.util[,user]','vm.memory.size[available]','vm.memory.size[total]']
	items_list=[]
	#print response['result']	
	for i in response['result']:
		k=i['key_']
		if k in str(bzlist):
			items_list.append(i.values()[0])
	namenew=['cpu','memoryfree','memeorytotal']
	return dict(zip(namenew,items_list))

if __name__=='__main__':
	a=get_items_id('10242')
	print a
