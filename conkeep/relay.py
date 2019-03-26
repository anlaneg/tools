#-*- coding:utf-8 -*-

import fcntl
import os
from socket import *
import subprocess
from time import ctime

import cmdbase
from conf import RelayConf
import conn
from event import Event
from event import EventLoop
from exception import DisConnectException
from exception import OpenBashException


class RelayServerCommandExecuteEvent(Event):
    def __init__(self,fd,data):
        super(RelayServerCommandExecuteEvent,self).__init__(fd,data)
    
    def run_read_event(self):
        data = self.socket.recv(self.data['server'].conf.buffsize).decode()
        if not data:
            return
        try:
            output=self.data['server'].execute_command(data)
            self.socket.send('%s\n' % output.encode())
        except DisConnectException as e:
            self.socket.send('%s\n' % str(e).encode())
            EventLoop.del_revent(self)
            self.socket.close()
        except OpenBashException as e:
            EventLoop.del_revent(self)
            output=self.data['server'].open_bash(e.client_id,self.socket)
            self.socket.send(output.encode())
            
    
    def run_exception_event(self):
        self.socket.send('found error,disconnect\n'.encode())
        EventLoop.del_revent(self)
        self.socket.close()
              
class RelayServerAcceptEvent(Event):
    def __init__(self,fd,data):
        super(RelayServerAcceptEvent,self).__init__(fd,data)
    
    def run_read_event(self):
        print('Wait for connection ...')
        client_socket,addr=self.socket.accept()
        print("Connection from :",addr)
        dict={'addr':addr,
              'server':self.data['server']
            }
        self.data['server'].connects.add_connect((client_socket,addr))
        EventLoop.add_revent(RelayServerCommandExecuteEvent(client_socket,dict))
    
    def run_exception_event(self):
        raise NotImplementedError

class BashReadEvent(Event):
    def __init__(self,file,data):
        #set fd to noblocking
        #fd = file.fileno()
        #flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        #fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        super(BashReadEvent,self).__init__(file,data)
    
    def run_read_event(self):
        while True:
            ret=self.socket.read(1024)
            print("read stdout...",ret)
            if not ret:
                break
            #print("read stdout...",ret)
            self.data['client'].send(ret)
            if len(ret) < 1024:
                break
    
    def run_exception_event(self):
        raise NotImplementedError
    
class BashWriteEvent(Event):
    def __init__(self,file,data):
        super(BashWriteEvent,self).__init__(file,data)
    
    def run_read_event(self):
        while True:
            ret = self.socket.recv(1024).decode()
            if not ret:
                break
            print("write to bash",ret)
            self.data['bash'].write(ret)
            if len(ret) < 1024:
                break
    
    def run_exception_event(self):
        raise NotImplementedError
    
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
    
    def run_eventloop(self):
        dict={
              'server':self
            }
        EventLoop.add_revent(RelayServerAcceptEvent(self.socket,dict))
        EventLoop.event_loop()
    
    def open_bash(self,client_id,socket):
        bash=subprocess.Popen([self.conf.bash_path],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  stdin=subprocess.PIPE, shell = False)
        
        dict={
              'client':socket
              }
        EventLoop.add_revent(BashReadEvent(bash.stdout,dict))
        EventLoop.add_revent(BashWriteEvent(socket,data={'bash':bash.stdin}))
        return "open the shell of client %s" % client_id
    
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
    #RelayServer(RelayConf()).setup().run_bash()
    RelayServer(RelayConf()).setup().run_eventloop()