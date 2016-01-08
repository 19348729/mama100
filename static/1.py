#!/usr/bin/env python
f=open('2.txt','r')
for i in f.readlines():
	n=i.replace(i[-1],'<br>')
	print n
