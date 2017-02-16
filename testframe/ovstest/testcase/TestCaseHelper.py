from ovstest.frame import testcase as testcase

class TestCaseHelper(testcase.TestCase):
    def __init__(self):
        super(TestCaseHelper,self).__init__(self.__class__.__name__)
