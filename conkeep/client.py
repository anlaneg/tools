#-*- coding:utf-8 -*-

from socket import *
from conf import ClientConf

class Client(object):
    def __init__(self,conf):
        self.conf = conf
        self.socket = -1
        pass
    
    def run(self):
        while True:
            data = raw_input(">")
            if not data:
                break
            self.socket.send(data.encode())
            data = self.socket.recv(self.conf.buffsize).decode()
            if not data:
                break
            print(data)
        self.socket.close()
        pass
    
    def setup(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((self.conf.relay_host,self.conf.relay_port))
        return self


if __name__ == "__main__":
    Client(ClientConf()).setup().run()