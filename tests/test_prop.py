
import unittest

from easyvar.prop import Prop
from easyvar.mixins import PropMixin
from easyvar import Void

class Test_module_prop(unittest.TestCase):
    def setUp(self):
        # init
        pass
    
    def tearDown(self):
        # destruct
        pass

    def test_Prop(self):
        with self.assertRaises(ValueError):
            Prop(readonly=Prop.RO_WEAK | Prop.RO_STRONG)

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

    def test_del(self):
        class B(PropMixin):
            name = 'John Doe'
            employer = Prop('Google', readonly=True) # normal Prop property
            ceo = Prop("Bill Gates", readonly=True, undead=True)
            mark = Prop("Mark Twane", readonly=Prop.RO_CLASS)
            pepe = Prop("Some Name", readonly=Prop.RO_CLASS|Prop.RO_WEAK)
            alu = Prop("Potato", readonly=Prop.RO_WEAK, undead=Prop.UD_CLASS)
            potol = Prop('Some vegetable', readonly=Prop.RO_CLASS|Prop.RO_STRONG, undead=Prop.UD_CLASS|Prop.UD_INSTANCE)
        b = B()
        del B.name
        with self.assertRaises(AttributeError):
            B.name
        
        del B.employer # ok readonly but deletable
        with self.assertRaises(AttributeError):
            B.employer

        with self.assertRaises(AttributeError):
            del B.ceo
        B.Props.Defaults.ceo # not deletable so was not deleted
        with self.assertRaises(AttributeError):
            del b.ceo
        with self.assertRaises(AttributeError):
            B.ceo = 5
        assert B.Props.Conf.ceo.is_readonly_for_class == True

        # mark is readonly for class only
        with self.assertRaises(AttributeError):
            B.mark = 'Overwritten'
        # while not readonly for instance object
        b.mark = 'Overwritten'
        assert b.mark == 'Overwritten'

        # pepe is readonly for class and weak readonly for instance object
        with self.assertRaises(AttributeError):
            B.pepe = 'Some other name'
        with self.assertRaises(AttributeError):
            b.pepe = 'Readonly again'
        # but pepe is weak readonly
        b._pepe = "Overwritten" # using internal variable
        assert b.pepe == "Overwritten"

        # alu is weak readonly and undead by class
        with self.assertRaises(AttributeError):
            del B.alu # undead for class
        with self.assertRaises(AttributeError):
            del b.alu # internal variable does not exist yet
            # internal variable is only created after changing the value at least once.
        with self.assertRaises(AttributeError):
            b.alu = 'Potol' # not ok, alu is weak readonly
        b._alu = 'Potol' # ok
        assert b.alu == 'Potol'
        # now that the internal variable exists, it can be deleted
        del b.alu
        # now alu is back to its default value:
        assert b.alu == 'Potato'

        with self.assertRaises(AttributeError):
            del B.potol
        with self.assertRaises(AttributeError):
            del b.potol
        with self.assertRaises(AttributeError):
            B.potol = 3
        with self.assertRaises(AttributeError):
            b.potol = 3


    def test_Prop_readonly_for_class(self):
        class B(PropMixin):
            mark = Prop("Mark Twane", readonly=Prop.RO_CLASS)
        with self.assertRaises(AttributeError):
            B.mark = 2

    def test_Prop_store_default(self):
        class B(PropMixin):
            begun = Prop('Brinjal', store_default=False)
        
        with self.assertRaises(AttributeError):
            B.Props.Defaults.begun
    
    def test_Prop_Void_Value(self):
        class B(PropMixin):
            mark = Prop(Void)
        b = B()
        B.mark # is the property object itself
        with self.assertRaises(AttributeError):
            b.mark # Void is non-existent value
    
    def test_Prop_Constness(self):
        p = Prop()
        with self.assertRaises(AttributeError):
            p.value = 3
        with self.assertRaises(AttributeError):
            del p.value
        with self.assertRaises(AttributeError):
            p.is_readonly = False
        with self.assertRaises(AttributeError):
            p.is_readonly_for_class = False
        with self.assertRaises(AttributeError):
            p.is_readonly_weak = 3
        with self.assertRaises(AttributeError):
            p.is_undead_for_class = 3
        with self.assertRaises(AttributeError):
            p.is_undead_for_instance = 2
        
        # dels
        with self.assertRaises(AttributeError):
            del p.is_readonly
        with self.assertRaises(AttributeError):
            del p.is_readonly_for_class
        with self.assertRaises(AttributeError):
            del p.is_readonly_weak
        with self.assertRaises(AttributeError):
            del p.is_undead_for_class
        with self.assertRaises(AttributeError):
            del p.is_undead_for_instance
        with self.assertRaises(AttributeError):
            del p.value
        with self.assertRaises(AttributeError):
            del p.var_name_prefix
        with self.assertRaises(AttributeError):
            del p.var_name_suffix
        
        # some random new attribute
        p.some_random___something = 4
        with self.assertRaises(AttributeError):
            p.some_random___something = 4
        with self.assertRaises(AttributeError):
            del p.some_random___something

        # constants

        with self.assertRaises(AttributeError):
            Prop.RO_STRONG = 2
        with self.assertRaises(AttributeError):
            Prop.RO_WEAK = 1
        with self.assertRaises(AttributeError):
            Prop.RO_WEAK = 3
        with self.assertRaises(AttributeError):
            Prop.UD_INSTANCE = 1
        with self.assertRaises(AttributeError):
            Prop.UD_INSTANCE = 2



if __name__ == '__main__':
    unittest.main(verbosity=2)
