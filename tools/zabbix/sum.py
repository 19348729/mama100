#!/usr/bin/env python


from hostid import *
from itemsid import *
from graph import *
from clock_to_time import *

def valuetokey(value):
	for k,v in items_id.itemes():
		if value == v:
			 return k



def get_result(ip):
	sum_result=[]
	host_id=get_host_id(ip)
	items_id=get_items_id(host_id)
	sum_result.append(get_items_history_cpu(items_id['cpu']))
	sum_result.append(get_items_history_mem(items_id['memory']))
	result_dict={}
	clock_list=[]
	value_list=[]
	sum_dict={}
	for i in sum_result:
		print "test :%s " %i
		for j in i:
			print "j is #######%s" %j
			value_list.append(j['value'])
			print "value_list is ####%s" %value_list
			clock_list.append(clock_to_time(float(j['clock'])))
			#clock_list.append(j['clock'])
		sum_dict['value']=value_list
		sum_dict['clock']=clock_list
		result_dict[j['itemid']]=sum_dict
		#result_dict[items_id.keys()]=sum_dict
		print "sum_dict is %s" %j['itemid']
		clock_list=[]
		value_list=[]
		sum_dict={}
				
	return  result_dict
if __name__=='__main__':
	a=get_result('192.168.233.3')
	print	a
