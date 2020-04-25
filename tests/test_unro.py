
import unittest
import copy
import inspect

from easyvar import unro
from easyvar.utils import deepcopy

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
        # class undead
        class B(unro.ClassUndead): pass
        class C(unro.ClassUndeadMap): pass

        self._undead_test(B)
        with self.assertRaises(AssertionError):
            self._undead_test(B())
        self._undead_map_test(C)
        with self.assertRaises(AssertionError):
            self._undead_map_test(C())
        
        # total undead
        class B(unro.Undead): pass
        class C(unro.UndeadMap): pass

        self._undead_test(B())
        self._undead_test(B)
        self._undead_map_test(C())
        self._undead_map_test(C)
    
    def _readonly_test(self, obj):
        obj.a = 3
        with self.assertRaises(AttributeError):
            obj.a = 2
        with self.assertRaises(TypeError):
            obj['b'] = 3
    
    def _readonly_map_test(self, obj):
        obj.a = 3
        with self.assertRaises(AttributeError):
            obj.a = 2
        obj['b'] = 3
        with self.assertRaises(AttributeError):
            obj['b'] = 2
    
    def test_readonly(self):
        # class readonly
        class B(unro.ClassReadonly):pass
        class C(unro.ClassReadonlyMap):pass

        # total readonly
        class D(unro.Readonly):pass
        class E(unro.ReadonlyMap):pass

        self._readonly_test(B)
        with self.assertRaises(AssertionError):
            self._readonly_test(B())

        self._readonly_test(D)
        self._readonly_test(D())

        self._readonly_map_test(C)
        with self.assertRaises(AssertionError):
            self._readonly_map_test(C())

        self._readonly_map_test(E)
        self._readonly_map_test(E())

    def _unro_test(self, obj):
        self._undead_test(deepcopy(obj))
        self._readonly_test(deepcopy(obj))
    
    def _unro_map_test(self, obj):
        self._readonly_map_test(deepcopy(obj))
        self._undead_map_test(deepcopy(obj))
    
    def test_unro(self):
        # class unro
        class B(unro.ClassUnro): pass
        class C(unro.ClassUnroMap): pass

        # Total unro
        class D(unro.Unro): pass
        class E(unro.UnroMap): pass

        self._unro_test(B)
        with self.assertRaises(AssertionError):
            self._unro_test(B())

        self._unro_test(D)
        self._unro_test(D())

        self._unro_map_test(C)
        with self.assertRaises(AssertionError):
            self._unro_map_test(C())

        self._unro_map_test(E)
        self._unro_map_test(E())

    def test_ConstClass(self):
        class B(unro.ConstClass):pass

        self._unro_test(B)
        with self.assertRaises(AttributeError):
            self._unro_test(B())

    def test_ConstClassMap(self):
        class B(unro.ConstClassMap):pass

        self._unro_map_test(B)
        with self.assertRaises(AttributeError):
            self._unro_map_test(B())




if __name__ == '__main__':
    unittest.main(verbosity=2)
