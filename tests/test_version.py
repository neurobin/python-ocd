
import unittest

from easyvar.version import __version__

class Test_version(unittest.TestCase):
    def setUp(self):
        # init
        pass
    
    def tearDown(self):
        # destruct
        pass
    
    def test_version(self):
        self.assertTrue(isinstance(__version__, str))
        self.assertTrue(__version__)
        self.assertTrue(len(__version__) >= 5)



if __name__ == '__main__':
    unittest.main(verbosity=2)
