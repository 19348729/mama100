#!/usr/bin/env python
import socket
import paramiko


'''
test ssh hostname use username and password 
return True-----ssh ok
return False----ssh not ok password may be error
return "ssh port error" ----port may be error

'''

def auth_test(username,hostname,password,port=22):
    try:
        biaoji=0
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception, e:
		biaoji="ssh port error"
		return biaoji

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            biaoji="link error ssh error"
            return biaoji
        t.auth_password(username,password)
        if t.is_authenticated():
            biaoji="auth ok"
        else:
            biaoji="username or password error"
        return biaoji
    except Exception, e:
        biaoji="username or password error"
        return biaoji
    try:
        t.close()
    except:
        pass

if __name__=="__main__":
	username = 'root'
	hostname='192.168.234.139'
	password='roots1234'
	port = 22
	result=auth_test(username,hostname,password,port)    
	print result
