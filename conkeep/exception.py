class DisConnectException(Exception):
    def __init__(self,msg):
        super(DisConnectException,self).__init__(msg)