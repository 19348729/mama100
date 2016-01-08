#!/usr/bin/env python
import socket
import paramiko
import sys,os

username = 'root'
hostname='192.168.234.139'
password='root1234'
port = 22
def auth_test(username,hostname,password,port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception, e:
        print '*** Connect failed: ' + str(e)
        traceback.print_exc()
        sys.exit(1)

    try:
        biaoji=0
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            print '*** SSH negotiation failed.'
            biaoji=1
            return biaoji
            sys.exit(1)
        t.auth_password(username,password)
        if t.is_authenticated():
            biaoji=True
        else:
            biaoji=False
        return biaoji
    except Exception, e:
        biaoji=False
        return biaoji
    try:
        t.close()
    except:
        pass
    sys.exit(1)

result=auth_test(username,hostname,password,port)
print result