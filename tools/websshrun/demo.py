import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import threading
import time
import traceback

import paramiko
import interactive

def demorun():

    # setup logging
    paramiko.util.log_to_file('demo.log')

    username = 'root'
    hostname='192.168.233.2'
    password='root1234'
    port = 22

    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception, e:
        print '*** Connect failed: ' + str(e)
        traceback.print_exc()
        sys.exit(1)

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            print '*** SSH negotiation failed.'
            sys.exit(1)

        t.auth_password(username,password)
        if not t.is_authenticated():
            print '*** Authentication failed. :('
            t.close()
            sys.exit(1)

        chan = t.open_session()
        chan.get_pty()
        chan.invoke_shell()
        print '*** Here we go!'
        print
        interactive.posix_shell(chan,username,hostname)
        chan.close()
        t.close()

    except Exception, e:
        print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)


