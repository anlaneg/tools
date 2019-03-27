#encoding:utf-8
import select

class Event(object):
    EVENT_MODE_READ = 1
    EVENT_MODE_WRITE = 2
    EVENT_MODE_EXCEPTION = 3
    
    def __init__(self,socket,data):
        self.socket = socket
        self.data=data
    
    def run_read_event(self):
        raise NotImplementedError
    
    def run_write_event(self):
        raise NotImplementedError
    
    def run_exception_event(self):
        raise NotImplementedError
    
    def run(self,mode):
        if mode == Event.EVENT_MODE_READ:
            self.run_read_event()
        elif mode == Event.EVENT_MODE_WRITE:
            self.run_write_event()
        elif mode == Event.EVENT_MODE_EXCEPTION:
            self.run_exception_event()
        else:
            raise NotImplementedError
    
    def get_fd(self):
        if self.socket < 0:
            raise Exception("fd(%s) < 0" % self.socket)
        return self.socket
    
    def destroy(self):
        pass

class EventLoop(object):
    __instance = None
    def __new__(cls, *args, **kwargs):  
        # 这里不能使用__init__，因为__init__是在instance已经生成以后才去调用的
        if cls.__instance is None:
            cls.__instance = super(EventLoop, cls).__new__(cls, *args, **kwargs)
            
            #do init
            cls.__instance.revents = {}
            cls.__instance.wevents = {}
        return cls.__instance
    
    def _add_event(self,event,mode):
        dict=None
        if mode == Event.EVENT_MODE_READ:
            dict=self.revents
        elif mode == Event.EVENT_MODE_WRITE:
            dict=self.wevents
        else:
            raise NotImplementedError
        
        key = event.get_fd()
        if key in dict:
            raise Exception("duplicate event key")
        dict[key] = event
        
    def _del_event(self,event,mode):
        dict=None
        if mode == Event.EVENT_MODE_READ:
            dict=self.revents
        elif mode == Event.EVENT_MODE_WRITE:
            dict=self.wevents
        else:
            raise NotImplementedError
        
        key = event.get_fd()
        if key in dict:
            return dict.pop(key)
        return None
    
    @classmethod
    def add_revent(cls, event):
        cls.__instance._add_event(event,Event.EVENT_MODE_READ)
    
    @classmethod    
    def add_wevent(cls, event):
        cls.__instance._add_event(event,Event.EVENT_MODE_WRITE)
        
    @classmethod
    def add_rwevent(cls,event):
        cls.__instance.add_revent(event)
        cls.__instance.add_wevent(event)
    
    @classmethod
    def del_revent(cls,event):
        return cls.__instance._del_event(event,Event.EVENT_MODE_READ)
    
    @classmethod    
    def del_wevent(cls,event):
        return cls.__instance._del_event(event,Event.EVENT_MODE_WRITE)
    
    @classmethod
    def del_rwevent(cls,event):
        return  (cls.__instance._del_event(event,Event.EVENT_MODE_READ),cls.__instance._del_event(event,Event.EVENT_MODE_WRITE))
      
    def run(self,interval=None):
        inputs=[i.get_fd() for i in self.revents.values()]
        outputs=[i.get_fd() for i in self.wevents.values()]
        print(inputs,outputs)
        
        if len(inputs) + len(outputs) > 0:
            readable, writable, exceptional = select.select(inputs, outputs, [],interval)
            
            print(readable,writable,exceptional)
            for r in readable:
                if r not in self.revents:
                    continue
                self.revents[r].run(Event.EVENT_MODE_READ)
                
            for w in writable:
                if r not in self.wevents:
                    continue
                self.wevents[w].run(Event.EVENT_MODE_WRITE)
                
            for e in exceptional:
                dict=None
                if e in self.revents:
                    dict = self.revents
                elif e in self.wevents:
                    dict = self.wevents
                else:
                    raise Exception("unkown exception fd %s" % e)
                dict[e].run(Event.EVENT_MODE_EXCEPTION)
        else:
            #todo wait interval ?
            pass
    
    @classmethod
    def event_loop(cls):
        while True:
            cls.__instance.run()
        
EventLoop()        
