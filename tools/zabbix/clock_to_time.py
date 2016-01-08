#!/usr/bin/env python

'''
this program is change zabbix clock value to time show
eg.1448635631 :'2015-11-27 22:47:11'

'''
import time
def clock_to_time(value):
	format = '%H:%M:%S'
	temp=time.localtime(value)
	new_time=time.strftime(format,temp)
	return new_time

if __name__=='__main__':
	print clock_to_time(1448954252)
	
