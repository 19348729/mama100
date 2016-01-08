#!/usr/bin/env python
__author__ = 'DELL'
# from gevent import monkey
# print "nb"
# monkey.patch_all()

from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
# from django_websocket import *
from dwebsocket import require_websocket
## from geventwebsocket.handler import WebSocketHandler
# from gevent.pywsgi import WSGIServer

# from django_websocket.decorators import websocket

def webssh_index(request):

    return render_to_response('webssh_index.html')

@require_websocket
def webssh_connect(request):
    print "begin  "
    print request.websocket
    print "han"
    message = request.websocket.wait()
    if 'hello' in message:


        request.websocket.send(message+'NBBBB')
    else:
        request.websocket.send('wokao')

    print "end"






