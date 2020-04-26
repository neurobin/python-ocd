
import unittest
import copy

from easyvar.types import SingletonMeta, VoidType, Void

class Test_Types(unittest.TestCase):
    def setUp(self):
        # init
        pass

    def tearDown(self):
        # destruct
        pass

    def test_SingletonMeta(self):
        class B(metaclass=SingletonMeta):
            pass

        b = B()

    def test_VoidType(self):
        V = VoidType()
        self.assertTrue(V is Void) # singleton
        self.assertTrue(copy.copy(V) is Void) # singleton
        self.assertTrue(copy.deepcopy(V) is Void) # singleton

    def test_Void(self):
        self.assertFalse(Void)
        self.assertFalse(len(Void))
        self.assertFalse(Void is None)
        self.assertFalse(Void is True)
        self.assertFalse(Void is False)
        self.assertTrue(isinstance(Void, VoidType))
        self.assertTrue(copy.copy(Void) is Void)
        self.assertTrue(copy.deepcopy(Void) is Void)
        self.assertTrue(len(Void) == 0)
        with self.assertRaises(NotImplementedError):
            Void.attr = 3
        with self.assertRaises(NotImplementedError):
            Void['attr'] = 3



if __name__ == '__main__':
    unittest.main(verbosity=2)
