#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2
# based url and required header
url1 = "http://192.168.234.84/zabbix/api_jsonrpc.php"
password='mama100'

header = {"Content-Type":"application/json"}
# auth user and password
def get_auth_id():
	data = json.dumps(
	{
	   "jsonrpc": "2.0",
	   "method": "user.login",
	   "params": {
	   "user": "Admin",
	   "password":password 
	},
	"id": 0
	})
	# create request object
	request = urllib2.Request(url1,data)
	for key in header:
	   request.add_header(key,header[key])
	# auth and get authid
	try:
	   result = urllib2.urlopen(request)
	except URLError as e:
	   print "Auth Failed, Please Check Your Name AndPassword:",e.code
	else:
	   response = json.loads(result.read())
	   result.close()
	return response['result']

if __name__=='__main__':
	a=get_auth_id()
	print type(a)
