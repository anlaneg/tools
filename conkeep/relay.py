#-*- coding:utf-8 -*-

from socket import *
from time import ctime
from conf import RelayConf
from exception import DisConnectException
import cmdbase
import conn
import subprocess
      
class RelayServer(object):
    def __init__(self,conf):
        self.conf = conf
        self.socket = -1
        self.commands= cmdbase.CommandCollection()
        self.commands._load_commands(cmdbase)
        self.connects = conn.ConnectCollection()
        pass
    
    def execute_command(self,input):
        class context(object):
            def __init__(self,cmd,conns):
                self.commands = cmd
                self.connects = conns
        return self.commands.execute(context(self.commands.commands,self.connects.conns),input)
    
    def run_bash(self):
        while True:
            print('Wait for connection ...')
            client_socket,addr = self.socket.accept()
            print("Connection from :",addr)
            self.connects.add_connect((client_socket,addr))
            bash=subprocess.Popen([self.conf.bash_path],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  stdin=subprocess.PIPE, shell = False)
            
            while True:
                data = client_socket.recv(self.conf.buffsize).decode()
                if not data:
                    continue
                ret=bash.poll()
                if ret:
                    #close connect
                    print("exit....")
                    client_socket.close()
                    break
                stdout,stderr=bash._communicate(input=data)
                #print(stdout,stderr)
                if stdout:
                    client_socket.send(stdout.encode())
                if stderr:
                    client_socket.send(stderr.encode())
                #for i in bash.stdout.readlines():
                #    client_socket.send(i.encode())
                    
                #for i in bash.stderr.readlines():
                #    client_socket.send(i.encode())      
                    
    def run(self):
        while True:
            print('Wait for connection ...')
            client_socket,addr = self.socket.accept()
            print("Connection from :",addr)
            self.connects.add_connect((client_socket,addr))

            while True:
                data = client_socket.recv(self.conf.buffsize).decode()
                if not data:
                    continue
                try:
                    output=self.execute_command(data)
                    #client_socket.send(('[%s]\n%s' % (ctime(),output)).encode())
                    client_socket.send('%s\n' % output.encode())
                except DisConnectException as e:
                    client_socket.send('%s\n' % str(e).encode())
                    client_socket.close()
                    break;
        self.socket.close()
        pass
    def setup(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
        self.socket.bind((self.conf.host,self.conf.port))
        self.socket.listen(3)
        return self
        
        
if __name__ == "__main__":
    #RelayServer(RelayConf()).setup().run()
    RelayServer(RelayConf()).setup().run_bash()