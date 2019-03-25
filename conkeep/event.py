
import select


class Event(object):
    def __init__(self,fd,data):
        self.fd = fd
        self.data=data
    
    def run(self,mode):
        raise NotImplementedError
    
    def get_fd(self):
        return self.fd
    pass


class EventLoop(object):

    def __init__(self):
        self.revents = {}
        self.wevents = {}
        pass

    def destroy(self):
        pass
    
    def add_revent(self, key, event):
        if key in self.revents:
            raise Exception("duplicate event key")
        self.revents[key] = event
        
    def add_wevent(self, key, event):
        if key in self.wevents:
            raise Exception("duplicate event key")
        self.wevents[key] = event
    
    def del_revent(self, key):
        if key in self.revents:
            event = self.revents.pop(key)
            event.destroy()
            
    def del_wevent(self,key):
        if key in self.wevents:
            event = self.wevents.pop(key)
            event.destroy()
            
    def run(self,interval=None):
        inputs=[i.get_fd() for i in self.revents.values()]
        outputs=[i.get_fd() for i in self.wevents.values()]
        
        if len(inputs) + len(outputs) > 0:
            readable, writable, exceptional = select.select(inputs, outputs, None,interval)
            for r in readable
        else:
            #wait interval
        
        
