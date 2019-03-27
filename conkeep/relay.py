#-*- coding:utf-8 -*-

import fcntl
import os
from socket import *
import subprocess
from time import ctime
import termios
import sys
import tty
import signal
import struct
import time

import cmdbase
from conf import RelayConf
import conn
from event import Event
from event import EventLoop
from exception import DisConnectException
from exception import OpenBashException
import metty


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
            #EventLoop.del_revent(self)
            output=self.data['server'].open_bash(e.client_id,self.socket)
            self.socket.send(output.encode())
        except Exception as e:
            self.socket.send(str(e))
            
    
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
        metty.setup_bash(["bash",'-i'],socket)
        return "disconnect the shell of client %s" % client_id
    
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