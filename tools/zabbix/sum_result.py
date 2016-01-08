#!/usr/bin/env python


from hostid import *
from itemsid import *
from graph import *
from clock_to_time import *

def valuetokey(ip,value):
	host_id=get_host_id(ip)
	items_id=get_items_id(host_id)
	for k,v in items_id.items():
		if value == v:
			return k



def get_result(ip,limit=5):
    sum_result=[]
    host_id=get_host_id(ip)
    if host_id:
        items_id=get_items_id(host_id)
        sum_result.append(get_items_history_cpu(items_id['cpu'],limit))
        sum_result.append(get_items_history_mem(items_id['memoryfree'],limit))
        result_dict={}
        clock_list=[]
        value_list=[]
        sum_dict={}
        for i in sum_result:
            for j in i:
                value_list.append(j['value'])
                clock_list.append(clock_to_time(float(j['clock'])))
                #clock_list.append(j['clock'])
            sum_dict['value']=value_list
            sum_dict['clock']=clock_list
            result_dict[valuetokey(ip,j['itemid'])]=sum_dict
            #result_dict(j['itemid'])=sum_dict
            #result_dict[items_id.keys()]=sum_dict
            clock_list=[]
            value_list=[]
            sum_dict={}

    ######mem change to /G
        mem_list=result_dict['memoryfree']['value']
        temp_list=[]
        for mem in mem_list:
                temp_list.append(int(mem)/1024/1024/1024)
        result_dict['memoryfree']['value']=temp_list

        return  result_dict
    else:
        return False



if __name__=='__main__':
	a=get_result('192.168.233.3')
	print a
