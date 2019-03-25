#encoding:utf-8
import re
from exception import DisConnectException
class CommandCollection(object):
    __instance = None
    def __new__(cls, *args, **kwargs):  
        # 这里不能使用__init__，因为__init__是在instance已经生成以后才去调用的
        if cls.__instance is None:
            cls.__instance = super(CommandCollection, cls).__new__(cls, *args, **kwargs)
            
            #do init
            cls.__instance.pattern = re.compile(r'^\s*([\S]+)(.*?)$', re.M|re.I)
            cls.__instance.commands={}
        return cls.__instance
        
    def update(self,text,cmd):
        text = text.strip();
        self.commands[text]=cmd
        
    @classmethod
    def _parse_first_token(cls,input):
        m = cls.__instance.pattern.match(input)
        if len(m.groups()) != 2:
            raise Exception("syntax error:%s" % input)
        return (m.group(1),m.group(2))
    
    def _exectue(self,context,first_token,argments,input):
        if first_token in self.commands:
            ret= self.commands[first_token].parser(argments.lstrip())
            print("parse result",ret,argments,input)
            if ret[0]:
                return self.commands[first_token].execute(context,**ret[1])
            else:
                raise Exception(ret[1])
        else:
            raise Exception("can't find command %s" % first_token)
        
    @classmethod
    def execute(cls,context,input):
        try:
            first_token,argments = cls._parse_first_token(input)
            return cls.__instance._exectue(context,first_token,argments,input)
        except DisConnectException as e:
            raise e
        except Exception as e:
            return str(e)
    
    def _load_commands(self,cur_moudle):
        #print(cur_moudle)
        for i in dir(cur_moudle):
            if i.endswith('Command'):
                #print("load command '%s'" % i)
                getattr(cur_moudle,i)()
        #print(self.commands)
        for i in self.commands.keys():
            print("load command:'%s',class=%s" %(i,self.commands[i]))
    
class CommandBase(object):
    def __init__(self):
        name=self.__class__.__name__
        if not name.endswith("Command") or name == "Command":
            raise Exception("class name error,example <text>Command")
        cmd=name[:-7].lower()
        #print("find command text '%s'" % cmd)
        CommandCollection().update(cmd,self)

    def help(self):
        raise NotImplementedError
    
    def execute(self,context,**kwargs):
        raise NotImplementedError
    
    def parser(self,input):
        raise NotImplementedError

class HelpCommand(CommandBase):
    def __init__(self):
        super(HelpCommand,self).__init__()
        
    def help(self):
        return "help <command> show command help information"
    
    def execute(self,context,cmd):
        if cmd not in context.commands:
            return "command '%s' unkown" % cmd
        return "%s" %context.commands[cmd].help()
    
    def parser(self,input):
        cmd=input.strip().split(' ')[0]
        if len(cmd) > 0:   
            return (True,{'cmd':cmd})
        return (False,"syntax error:\n %s\n" % self.help())
       
class ListCommand(CommandBase):
    def __init__(self):
        super(ListCommand,self).__init__()
        
    def help(self):
        return "list all commands"
    
    def execute(self,context):
        output="";
        for i in context.commands.keys():
            output="%s%s:\t%s\n" % (output,i,context.commands[i].help())
        return output
    
    def parser(self,input):
        if len(input.strip()) != 0:
            return (False,"syntax error:\n %s\n" % self.help())
        return (True,{})
    
class QuitCommand(CommandBase):
    def __init__(self):
        super(QuitCommand,self).__init__()
        
    def help(self):
        return "close current session"
    
    def execute(self,context):
        raise DisConnectException("disconnect")
    
    def parser(self,input):
        if len(input.strip()) != 0:
            return (False,"syntax error:\n %s\n" % self.help())
        return (True,{})
    
class ShowCommand(CommandBase):
    def __init__(self):
        super(ShowCommand,self).__init__()
        
    def help(self):
        return "show all clients"
    
    def execute(self,context):
        output="";
        for i in context.connects.keys():
            output="%s%s:\t%s\n" % (output,i,context.connects[i][1])
        return output
    
    def parser(self,input):
        if len(input.strip()) != 0:
            return (False,"syntax error:\n %s\n" % self.help())
        return (True,{})
    
class OpenCommand(CommandBase):
    def __init__(self):
        super(OpenCommand,self).__init__()
        
    def help(self):
        return "open <client_id>  open the shell of client"
    
    def execute(self,context,client_id):
        print(context.connects)
        if client_id not in context.connects:
            return "We cant't find client %s\n" % client_id
        return "open the shell %s" % client_id
    
    def parser(self,input):
        client_id=input.strip().split(' ')[0]
        if len(client_id) > 0:   
            return (True,{'client_id':client_id})
        return (False,"syntax error:\n %s\n" % self.help())
    
class BashCommand(CommandBase):
    def __init__(self):
        super(BashCommand,self).__init__()
        
    def help(self):
        return "baseh test"
    
    def execute(self,context,client_id):
        print(context.connects)
        if client_id not in context.connects:
            return "We cant't find client %s\n" % client_id
        return "open the shell %s" % client_id
    
    def parser(self,input):
        client_id=input.strip().split(' ')[0]
        if len(client_id) > 0:   
            return (True,{'client_id':client_id})
        return (False,"syntax error:\n %s\n" % self.help())