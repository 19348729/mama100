#!/usr/bin/env python2.7

#coding=utf-8
import json
import urllib2
from auth import *

url1 = "http://192.168.234.84/zabbix/api_jsonrpc.php"

header = {"Content-Type":"application/json"}


auth_id=get_auth_id()

def get_items_history_cpu(itemid,limit=5):
	data = json.dumps(

	{

	   "jsonrpc":"2.0",

	   "method":"history.get",

	   "params":{

		  "output":"extend",
			"history":0,
			"itemids":itemid,
			"limit":limit
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
	return response['result']

def get_items_history_mem(itemid,limit=5):
    data = json.dumps(

	{

	   "jsonrpc":"2.0",

	   "method":"history.get",

	   "params":{

		  "output":"extend",
			"history":3,
			"itemids":itemid,
			"limit":limit
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
    return response['result']

if __name__=='__main__':
    a=get_items_history_cpu('37128')
    print a
    b=get_items_history_mem('37151')
    print b
