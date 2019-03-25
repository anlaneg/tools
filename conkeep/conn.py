
class ConnectCollection(object):
    def __init__(self):
        self.id = 0
        self.conns={}
        
    def add_connect(self,tuple):
        self.id += 1
        self.conns[str(self.id)] = tuple
        
    def close_connect(self,id):
        client_socket,addr=self.conns[id]
        print("close client %s",addr)
        client_socket.send('disconnect'.encode())
        client_socket.close()