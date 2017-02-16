
import os 
from ovstest.frame import importutil as import_util

def load():
    objs = []
    
    for f in os.listdir(os.path.dirname(__file__)):
        if f.startswith('_') or f.endswith('.pyc'):
            continue
        #print('load %s' % f)
        idx = f.find('.')
        if idx == -1:
            name = f
        else:
            name = f[0:idx]
        #filename must equal class name
        obj=import_util.load_class('%s.%s.%s' % (__package__,name,name))
        objs.append(obj)
    return objs