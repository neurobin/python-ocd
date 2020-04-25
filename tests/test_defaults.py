
import unittest

from easyvar import defaults

class Test_defaults(unittest.TestCase):
    def setUp(self):
        # init
        pass
    
    def tearDown(self):
        # destruct
        pass
    
    def test_nomodify(self):
        value = [{'d':[3]}]
        self.assertTrue(value is defaults.nomodify(value))



if __name__ == '__main__':
    unittest.main(verbosity=2)
