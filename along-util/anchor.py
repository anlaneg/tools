
import os
import sys

def get_root_path():
    return os.path.split(os.path.realpath(__file__))[0]

def modify_sys_path():
    root=get_root_path()
    sys.path=[root] + sys.path
    #print(sys.path)

def main_wrap(module,main='main'):
    modify_sys_path()
    mod= __import__(module)

    poperty=main.split('.')
    submod = mod
    for submod_name in poperty[:-1]:
        submod = getattr(submod,submod_name)
    
    getattr(submod,poperty[-1])()

