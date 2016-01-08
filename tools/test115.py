#!/usr/bin/python
import os
import sys
for i in range(1,106):
	k=os.system('ping -c 1 192.168.115.'+str(i))
	print k
	if k == 0:
		print "%s is  ok" %i
	else:
		output = open('open.txt', 'rw')
		print "%s is not ok" %i
		i.write('open.txt')
	
