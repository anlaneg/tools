
import ovstest.frame.testsuite

class TestCaseFailed(Exception):
    def __init__(self,stdout,stderr,is_pass):
        self.stdout=stdout
        self.stderr=stderr
        self.result=is_pass
    

class TestCase(object):
    def __init__(self,name):
        self.name = name;
        ovstest.frame.testsuite.get_instance().append(self)
    def get_name(self):
        return self.name
    
    def build_env(self):
        pass
    
    def clean_env(self):
        pass
    
    def test(self):
        raise TestCaseFailed("fail","fail",False)
    
    def run(self):
        self.build_env()
        self.test()
        self.clean_env()
    

