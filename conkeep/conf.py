
class RelayConf(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8989
        self.buffsize = 2048
        self.bash_path="/bin/bash"
        pass
    
class ClientConf(object):
    def __init__(self):
        self.relay_host = '127.0.0.1'
        self.relay_port = 8989
        self.buffsize = 2048
        pass