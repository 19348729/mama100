#!/usr/bin/env python2.7

#coding=utf-8
import json
import urllib2
from auth import *

url1 = "http://192.168.234.84/zabbix/api_jsonrpc.php"

header = {"Content-Type":"application/json"}

auth_id=get_auth_id()
def get_host_id(ip):
    data = json.dumps(

    {

       "jsonrpc":"2.0",

       "method":"host.get",

       "params":{

           "output":["hostid","itemids"],
            "filter":{"host":ip}
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

    if response['result']:
        return response['result'][0].values()[0]
    else:
        return False

if __name__=='__main__':
	a=get_host_id('192.168.115.31')
	print a
