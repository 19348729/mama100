#!/usr/local/bin/python
#*- coding: UTF-8 -*-
import os
import sys

def sum_list(list_a,list_all):
	list_all.append(list_a)

def mylister(currdir,list_all):
	for file in os.listdir(currdir):
		path=os.path.join(currdir,file)
		if not os.path.isdir(path):
			sum_list(path,list_all)
		else:
			mylister(path,list_all)
def get_dir_file(currdir):
	list_all=[]
	mylister(currdir,list_all)
	return list_all
if __name__=='__main__':
	print get_dir_file('/tmp/test/alipay')
