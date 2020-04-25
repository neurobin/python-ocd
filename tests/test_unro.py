
import unittest

from easyvar import unro

class Test_unro(unittest.TestCase):
    def setUp(self):
        # init
        pass
    
    def tearDown(self):
        # destruct
        pass
    
    def test_Object(self):
        pass
    
    def test_Base(self):
        class B(unro.Base):
            a = 2
            b = 3
            c = 4
        
        b = B()
        with self.assertRaises(AssertionError):
            self.assertTrue(len(b) == 3)
        b.a = 3
        b.b = 2
        b.c = 4
        self.assertTrue(len(b) == 3)
        for attribute_name in b:
            print("Printing attribute name: ", attribute_name)
    
    def test_Map(self):
        class B(unro.Map):
            a = 2
            b = 3
            c = 4
        
        b = B()
        with self.assertRaises(AssertionError):
            self.assertTrue(len(b) == 3)
        b.a = 3
        b.b = 2
        b.c = 4
        self.assertTrue(len(b) == 3)
        for attribute_name in b:
            print("Printing attribute name, value: ", (attribute_name, b[attribute_name]))
    
    def _undead_test(self, obj):
        obj.a = 3
        with self.assertRaises(AttributeError):
            del obj.a
        with self.assertRaises(TypeError):
            obj['b'] = 2
    
    def _undead_map_test(self, obj):
        obj.a = 3
        obj['b'] = 2
        with self.assertRaises(AttributeError):
            del obj.a
        with self.assertRaises(AttributeError):
            del obj['a']
        with self.assertRaises(AttributeError):
            del obj['b']
        with self.assertRaises(AttributeError):
            del obj.b
    
    def test_undead(self):
        class B(unro.ClassUndead): pass
        class C(unro.ClassUndeadMap): pass

        self._undead_test(B)
        with self.assertRaises(AssertionError):
            self._undead_test(B())
        self._undead_map_test(C)
        with self.assertRaises(AssertionError):
            self._undead_map_test(C())



if __name__ == '__main__':
    unittest.main(verbosity=2)
