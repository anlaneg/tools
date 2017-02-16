import sys
import ovstest.frame.testcase
from ovstest.testcase import _loader as loader
  
my_testsuite = None

class TestSuite(object):
    def __init__(self,stop_failed):
        self.testcases=[]
        self.failed=[]
        self.error=[]
        self.stop_failed = stop_failed

    def append(self,testcase):
        self.testcases.append(testcase)
    
    def _run(self):
        for test in self.testcases:
            try:
                test.run()
            except ovstest.frame.testcase.TestCaseFailed as e:
                self.failed.append(e)
                if self.stop_failed:
                    raise
            except Exception as e:
                self.error.append(e)
                if self.stop_failed:
                    raise
    
    def _load(self):
        return loader.load()
        
    def _make_error_strings(self,lists):
        string = ""
        for e in lists:
            string= string + str(e) +'\n'
        return string
    
    def _report(self,e=None):
        total  = len(self.testcases)
        failed = len(self.failed)
        error  = len(self.error)
        passed = total - failed - error
        
        if e:            
            self._error(
"""\t==================
\tresult:%s/%s pass
\t%s
            
            
\tfailed:%s/%s
\t%s
            
            
\terror:%s/%s
\t%s
            
            
\t==================\n"""  %(passed,total,self._make_error_strings([e]),
                          failed,total,self._make_error_strings(self.failed),
                          error,total,self._make_error_strings(self.error)))
        else:
            self._log(
"""\t==================
\tresult:%s/%s pass
            
\t:-)
\t==================\n""" % (passed,total))
        pass
    
    def _error(self,msg):
        sys.stdout.write(msg)
    
    def _info(self,msg):
        sys.stderr.write(msg)
    
    def run(self):
        self._load()
        size = len(self.testcases)
        if not size:
            self._error("no testcase load\n")
        else:
            self._info("we load testcase:%s\n" % size)
            for t in self.testcases:
                self._info('\t-->load testcase %s\n' % t.name)
        
        try:
            self._run()
            #success
            self._report()
        except Exception as e:
            
            #failed
            self._report(e)
    
def get_instance():
    global my_testsuite
    if not my_testsuite:
        my_testsuite = TestSuite(True)
    return my_testsuite
    