
import socket
import sys
import datetime,time
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = false

def posix_shell(chan,username,hostname):
    import select
    
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.setblocking(1)
        day_time=time.strftime('%Y_%m_%d')
        f=open('/mama100/mama100/static/test.txt','a')
        print "begin"
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    #if not chan.recv_ready():
                    #    print '\r\n*** EOF exit\r\n',
                    #    break
                    sys.stdout.write(x) 
                    f.write(str(x))
                    f.flush()
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)
        f.close()
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
