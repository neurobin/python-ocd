
import unittest

from ocd import defaults
from ocd.prop import Prop

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
    
    def test_always_valid(self):
        value = [{'d':[3]}]
        self.assertTrue(True is defaults.always_valid(value))
    
    def _common_varconf_test(self, VarConfClass):
        VarConfClass.get_conf # should exist
        conf = VarConfClass()
        p = conf.get_conf(None, None)
        self.assertTrue(isinstance(p, Prop) or p is None)

    def test_VarConfNone(self):
        self._common_varconf_test(defaults.VarConfNone)

    def test_VarConfAll(self):
        self._common_varconf_test(defaults.VarConfAll)



if __name__ == '__main__':
    unittest.main(verbosity=2)
