#!/usr/local/bin/python
#*- coding: UTF-8 -*-
import sys
import os
def lister(root,ml):
	for (thisdir,subshere,fileshere) in os.walk(root):
		print ('[' + thisdir + ']')
		for fname in fileshere:
			path=os.path.join(thisdir,fname)
			print (path)
lister(root,/tmp)

#if __name__=='__main__':
#	lister(sys.argv[1])
