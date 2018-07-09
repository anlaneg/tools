import socket
import sys
from subprocess import Popen, PIPE
import time

class Process(object):
    def __init__(self,cwd,cmd):
        self.cmd=cmd
        self.p = Popen(cmd,cwd=cwd, shell=True, stdout=PIPE, stderr=PIPE)
        print("create process %s" % self.p.pid)
    def kill(self):
        self.p.terminate()
        time.sleep(2)
        self.p.kill()

class Client(object):
    def __init__(self,server,port):
        self.server=server
        self.port=port
        
    def connect(self):
        obj = socket.socket()
        obj.connect((self.server,self.port))
        self.fd = obj
        
    def disconnect(self):
        self.fd.close()
        
    def notice(self,msg):
        self.fd.send(msg)
        data=self.fd.recv(1024)
        print("rcv reply %s" % data)

class Server(object):
    def __init__(self,port):
        
        self.port=port
    def listen(self):
        obj = socket.socket()
        obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
        obj.bind(("0.0.0.0",self.port))
        obj.listen(5)
        while True:
            conn,address = obj.accept()
            self.process(conn,address)
            conn.close()
    
    def process(self,conn,address):
        pass

class IperfClientRun(Client):
    def __init__(self,server,port):
        super(IperfClientRun,self).__init__(server,port)
    def __do_command(self,cmd):
        self.connect()
        self.notice(cmd)
        self.disconnect()
        
    def startUdp(self,output):
        self.__do_command("startudp %s" % output)
        
    def startTcp(self,output):
        self.__do_command('starttcp %s' % output)
        
    def stop(self):
        self.__do_command('stopall')
        
class IperfServerRun(Server):
    def __init__(self,port,cwd):
        super(IperfServerRun,self).__init__(port)
        self.proc=None
        self.cwd=cwd
        
    def process(self,conn,address):
        data=conn.recv(1024)
        if data.startswith("stop"):
            if self.proc:
                self.proc.kill()
                self.proc = None
                return
            else:
                raise Exception("need start process first")
        else:
            if self.proc:
                raise Exception("expect stop process")
            
        if data.startswith("startudp"):
            cmd="iperf -u -s -i 5 -p 9934 > %s" % data[8:]
            print("execute %s" % cmd)
            self.proc = Process(self.cwd,cmd)
            pass
        elif data.startswith("starttcp"):
            cmd="iperf -s -i 5 -p 9999 > %s" % data[8:]
            print("execute %s" % cmd)
            self.proc = Process(self.cwd,cmd)
            pass
        else:
            raise Exception("unknow command %s" % data)
        conn.sendall("do command %s ok" % data)

def test():
    if len(sys.argv) >= 2 and sys.argv[1]=="client":
        client = IperfClientRun(ip,port)
        client.startUdp("udp.txt")
        time.sleep(3)
        client.stop()
        client.startTcp("tcp.txt")
        time.sleep(3)
        client.stop()
    else:
        IperfServerRun(port,"/home/anlang/").listen()
if __name__ == "__main__":
    ip="127.0.0.1"
    port=33271
    dir="/home/anlang/"
    #test()
    #exit(0)
    if len(sys.argv) >= 4 and sys.argv[1]=="client":
        client = IperfClientRun(ip,port)
        if sys.argv[2] == "tcp":
            client.startTcp(sys.argv[3])
        else:
            client.startUdp(sys.argv[3])
    else:
        IperfServerRun(port,dir).listen()
    