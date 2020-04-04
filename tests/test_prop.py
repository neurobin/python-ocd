
import unittest

from easyvar.prop import Prop, PropMixin
from easyvar import Void

class PropModuleTest(unittest.TestCase):
    def setUp(self):
        # init
        pass
    
    def tearDown(self):
        # destruct
        pass

    def test_Prop(self):
        with self.assertRaises(ValueError):
            Prop(readonly_weak=True, readonly=True)

    def test_Prop_var_name_prefix(self):
        with self.assertRaises(ValueError):
            Prop(var_name_prefix='__')
        with self.assertRaises(ValueError):
            Prop(var_name_prefix='me_')
        with self.assertRaises(ValueError):
            Prop(var_name_prefix='')
        with self.assertRaises(ValueError):
            Prop(var_name_prefix=34)
        with self.assertRaises(ValueError):
            Prop(var_name_prefix=b'_')
        Prop(var_name_prefix='_me_') # OK

    def test_Prop_var_name_suffix(self):
        with self.assertRaises(ValueError):
            Prop(var_name_suffix='__')
        with self.assertRaises(ValueError):
            Prop(var_name_suffix=34)
        with self.assertRaises(ValueError):
            Prop(var_name_suffix=b'_')
        Prop(var_name_suffix='_me_') # OK
    
    def test_PropMixin_Prop(self):
        class B(PropMixin):
            a = Prop(4)
            b = Prop('bvalue', readonly=True)
            c = Prop([1,2,3], readonly=True)
            d = Prop({'a':3}, readonly_weak=True)
        
        # checking if values are right
        assert B.Props.Defaults.a == 4
        assert B.Props.Keys.a == 'a'
        assert B.Props.Ivan.a == '_a'
        assert isinstance(B.Props.Conf.a, Prop)

        # checking readonly status
        with self.assertRaises(AttributeError):
            B.Props.Defaults.a = 5
        with self.assertRaises(AttributeError):
            B.Props.Keys.a = 5
        with self.assertRaises(AttributeError):
            B.Props.Ivan.a = 5
        with self.assertRaises(AttributeError):
            B.Props.Conf.a = 5
        
        with self.assertRaises(AttributeError):
            B.Props = 5
        with self.assertRaises(AttributeError):
            B.Props.Keys = 5
        with self.assertRaises(AttributeError):
            B.Props.Defaults = 5
        with self.assertRaises(AttributeError):
            B.Props.Ivan = 5
        with self.assertRaises(AttributeError):
            B.Props.Conf = 5
        
        b = B()

        b.a = 'OK as a is not readonly'
        with self.assertRaises(AttributeError):
            b.b = 5 # not OK, b.b is readonly
        
        with self.assertRaises(AttributeError):
            B.Props.Ivan.b # readonly, so no internal variable
        
        B.Props.Ivan.d # weak readonly, so there is an internal variable

        b.c.append(4)
        assert b.c == [1,2,3,4]
    
    def test_PropMixin_VarConf(self):
        # TODO
        pass

    def test_PropMixin_Inheritance(self):
        # TODO
        pass
        




if __name__ == '__main__':
    unittest.main(verbosity=2)
