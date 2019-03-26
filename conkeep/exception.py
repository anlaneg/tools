class DisConnectException(Exception):
    def __init__(self,msg):
        super(DisConnectException,self).__init__(msg)
        

class OpenBashException(Exception):
    def __init__(self,id):
        self.client_id = id
        super(OpenBashException,self).__init__("open the shell %s" % self.client_id)