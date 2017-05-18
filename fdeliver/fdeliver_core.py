
import getopt
import sys
import optparse

class FdeliverArguments(object):
    def __init__(self):
        self.mode=None
        self.id=None
        self.next_host=None
    
    def set_id(self,id):
        self.id = id
        
    def set_mode(self,m):
        self.mode = m
        
    def set_next_host(self,n):
        if N is not None:
            nexts=N.split(',')
        self.next=nexts[0]
    
    def validate_host(self):
        #ip:port
        return False
    
    def validate(self):
        if self.mode not in ('src','dest','relay'):
            return False
        if self.mode != 'dest':
            if self.next is None:
                return False
        if self.id is None:
            return False
        return self.validate_host()
    
    def commandline(self):
        return "%s --id %s --mode %s --next %s" % (__file__,self.id,self.mode,self.next)
    
class FdeliverSocket(object):
    def __init__(self,fd):
        pass
    def read_cmd(self):
        return None,None
    def send_cmd(self,cmd,argments):
        raise Exception('fail')
    def relay_data(self,remote_fd):
        raise Exception('fail')
    def close(self):
        raise Exception('fail')
    def read_log(self):
        return None
    def write_log(self):
        return None
    
class FdeliverController(object):
    def __init__(self):
        super(FdeliverController,self).__init__()
    def dispatch_cmd(self):
        pass
    def _process_connect(self):
        pass
    def _process_close(self):
        pass
    def _process_ack(self):
        pass
    def _process_md5check(self):
        pass
    def _process_debug(self):
        pass
    
        
class FdeliverData(object):
    def __init__(self):
        super(FdeliverData,self).__init__()
        
class FdeliverServer(object):
    def __init__(self):
        pass
    def send(self,path):
        pass
    def connect(self):
        pass
    def disconnect(self):
        pass
    
def usage():
    print(u"""
    %s -m MODE -i ID -n NEXT_HOST
    -m / --mode [src|relay|dest]
    -i /--id fdeliver-id
    -n /--next next fdeliver server host
    -h /--help display this message
    """ % __file__)
    
def parse_options(options,unuse):
    args=FdeliverArguments()
    
    for name,value in options:
        if not name or name in ('-h',"--help"):
            usage()
            return
        if name in ('-m',"--mode"):
            args.set_mode(value)
            continue
        if name in ('-i','--id'):
            args.set_id(value)
            continue
        if name in ('-n','--next'):
            args.set_next(value)
            continue
    return args

def main():
    try:
        options,args = getopt.getopt(sys.argv[1:],"m:hi:p:n:",["help","next=","prev=","mode="])
        argments=parse_options(options,args)
    except getopt.GetoptError:
        usage()
        sys.exit()
    