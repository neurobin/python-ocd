
import unittest

from ocd import abc
from ocd.prop import Prop

class Test_abc(unittest.TestCase):
    def setUp(self):
        # init
        pass
    
    def tearDown(self):
        # destruct
        pass
    
    def test_abc_VarConf_NIMP(self): # NIMP: Not Itempemented
        class VarConf(abc.VarConf):
            pass
        
        with self.assertRaises(TypeError):
            VarConf.get_conf()
        with self.assertRaises(TypeError):
            VarConf.get_conf(None)
        with self.assertRaises(TypeError):
            VarConf.get_conf(None, None)

        with self.assertRaises(NotImplementedError):
            VarConf.get_conf(None, None, None)
        with self.assertRaises(TypeError):
            VarConf.get_conf(None, None, None, None)
        
        conf = VarConf()

        with self.assertRaises(TypeError):
            conf.get_conf()
        with self.assertRaises(TypeError):
            conf.get_conf(None)
        with self.assertRaises(NotImplementedError):
            conf.get_conf(None, None)
        with self.assertRaises(TypeError):
            conf.get_conf(None, None, None)
    
    def test_abc_VarConf_IMP(self): # IMP: implemented
        class VarConf(abc.VarConf):
            def get_conf(self, name, value):
                return None
        conf = VarConf()
        p = conf.get_conf(None, None)
        self.assertTrue(isinstance(p, Prop) or p is None)

        class VarConf(abc.VarConf):
            def get_conf(self, name, value):
                return Prop()
        conf = VarConf()
        p = conf.get_conf(None, None)
        self.assertTrue(isinstance(p, Prop) or p is None)

        class VarConf(abc.VarConf):
            def get_conf(self, name, value):
                return True
        conf = VarConf()
        p = conf.get_conf(None, None)
        with self.assertRaises(AssertionError):
            self.assertTrue(isinstance(p, Prop) or p is None)

        class VarConf(abc.VarConf):
            def get_conf(self, name, value):
                return self
        conf = VarConf()
        p = conf.get_conf(None, None)
        with self.assertRaises(AssertionError):
            self.assertTrue(isinstance(p, Prop) or p is None)
        



if __name__ == '__main__':
    unittest.main(verbosity=2)
