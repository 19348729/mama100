#!/usr/bin/env python
__author__ = 'DELL'
# from gevent import monkey
# print "nb"
# monkey.patch_all()

from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from dwebsocket import require_websocket
from tools.websshrun.demo import *

import threading
import sys
import subprocess
import time
import os
######on line show log file
g_output_log=[]
tailpid=''
pid_list=[]
def tailfiles(filename):
    print "file_name:%s"%filename
    global g_output_log
    global tailpid

    popen=subprocess.Popen(['bash','-c',filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    tailpid=popen.pid
    pid_list.append(tailpid)
    while True:
        line=popen.stdout.readline().strip()
        g_output_log.append(line)
        if subprocess.Popen.poll(popen) is not None:
            break

def webssh_index(request):

    return render_to_response('webssh_index.html')

@require_websocket
# def webssh_connect(request,filename):
#     print "file:%s"%filename
#     message = request.websocket.wait()
#     if message == 'start':
#         check=True
#         while check:
#             request.websocket.send('ok')
#             time.sleep(1)
#     elif message:
#         check=False
#         while True:
#             request.websocket.send('end')
#             time.sleep(3)






def webssh_connect(request,filename):
    message = request.websocket.wait()
    print "message is :%s"%message
    print "file:%s"%filename
    # file_name='/usr/local/nginx/logs/access.log'
    if 'start' in message:
        # cmd='tail -100f /usr/local/nginx/logs/access.log'
        cmd='tail -100f '+filename
        file_con=threading.Thread(target=tailfiles,args=([cmd]))
        file_con.start()
        while file_con.isAlive():
            if len(g_output_log)>0:
                log=g_output_log.pop()
                request.websocket.send(log)
        request.websocket.close()
    elif 'stop' in message:
        print "i kill it ....%s."%tailpid
        os.kill(tailpid,2)#####ctrl+c kill it
        request.websocket.send('i kill it')
        request.websocket.close()

####################web ssh run commd
def webrun_index(request):

    return render_to_response('webrun_index.html')
@require_websocket
def webrun(request,run_commd):
    message = request.websocket.wait()
    print "message is :%s"%message
    print "file:%s"%run_commd
    request.websocket.send(demorun())
    # if 'start' in message:
    #     file_con=threading.Thread(target=tailfiles,args=([cmd]))
    #     file_con.start()
    #     while file_con.isAlive():
    #         if len(g_output_log)>0:
    #             log=g_output_log.pop()
    #             request.websocket.send(log)
    #     request.websocket.close()




