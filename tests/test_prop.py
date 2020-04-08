
import unittest

from easyvar.prop import Prop, PropMixin
from easyvar import Void
from easyvar.defaults import VarConfNone, VarConfAll

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
    
    def test_PropMixin_Prop(self):
        class B(PropMixin):
            a = Prop(4)
            b = Prop('bvalue', readonly=True)
            c = Prop([1,2,3], readonly=True)
            d = Prop({'a':3}, readonly=Prop.RO_WEAK)
        
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
    
    def test_PropMixin_VarConf_Validity(self):
        # class that does not define any public attribute
        # will survive with a bad VarConf
        class B(PropMixin):
            class VarConf(): # does not inherit abc.VarConf
                def get_conf(self, n, v):
                    return None
        with self.assertRaises(TypeError):
            class B(PropMixin):
                class VarConf(): # does not inherit abc.VarConf
                    def get_conf(self, n, v):
                        return None
                my_property = 'value'

        class B(PropMixin):
            class VarConf(VarConfNone): # get_conf is inherited, so OK
                pass
            my_property = 'value'

        with self.assertRaises(TypeError):
            class B(PropMixin):
                VarConf = 4 # VarConf is a class
                my_property = 'value'
        
        with self.assertRaises(TypeError):
            class B(PropMixin):
                class VarConf(VarConfNone):
                    def get_conf(): # needs to accept name and value pair
                        pass
                my_property = 'value'
            

        class B(PropMixin):
            class VarConf(VarConfNone):
                @staticmethod
                def get_conf(n, v):
                    return None
            my_property = 'value'

        class B(PropMixin):
            class VarConf(VarConfNone):
                @classmethod
                def get_conf(cls, n, v):
                    return None
            my_property = 'value'

        with self.assertRaises(AssertionError):
            class B(PropMixin):
                class VarConf(VarConfNone):
                    def get_conf(self, n, v):
                        return True # needs to return None or Prop object
                my_property = 'value'
        
        # OK
        class B(PropMixin):
            class VarConf(VarConfNone):
                def get_conf(self, n, v):
                    return None
            my_property = 'value'
        
        # OK
        class B(PropMixin):
            class VarConf(VarConfNone):
                def get_conf(self, n, v):
                    return Prop()
            my_property = 'value'
    
    def test_PropMixin_VarConf_Uses(self):
        class B(PropMixin):
            class VarConf(VarConfNone):
                def get_conf(self, n, v):
                    return Prop(readonly=True)

            name = 'John Doe' # readonly
            employer = Prop('Google') # not readonly
        
        b = B()
        with self.assertRaises(AttributeError):
            b.name = 'Me' # Fail
        
        b.employer = 'Facebook' # OK


        class B(PropMixin):
            class VarConf(VarConfNone):
                def get_conf(self, n, v):
                    if n.endswith('_ro'):
                        return Prop(readonly=True)
                    elif n.endswith('_wro'):
                        return Prop(readonly=Prop.RO_WEAK)
                    elif n.endswith('_nd'):
                        return Prop(undead=True)
                    elif n.endswith('_rond'):
                        return Prop(undead=True, readonly=True)
                    elif v == 'Shady Company': # attribute with value 'Shady Company' will be readonly and undeletable
                        return Prop(undead=True, readonly=True)
                    elif n.endswith('_p') or n.endswith('_var'):
                        return Prop()
                    else:
                        return None

            name_ro = 'John Doe' # readonly
            employer_wro = 'Google' # weak readonly
            employerID_nd = '34242342432' # not deletable
            securityID_rond = '3424234312343' # readonly and not deletable
            employer = 'Shady Company' # attribute with value 'Shady Company' is readonly and undeletable
            current_location_p = 'Some street' # normal property
            some_var = 34
            current_status = 'some status' # normal attribute not property
        
        b = B()
        
        with self.assertRaises(AttributeError):
            b.name_ro = 'John Doe' # not OK
        
        with self.assertRaises(AttributeError):
            b.employer_wro = 'Microsoft' # not OK
        b._employer_wro = 'Microsoft' # OK, as employer_wro is weak readonly
        assert b.employer_wro == 'Microsoft' # employer_wro has changed.

        with self.assertRaises(AttributeError):
            del b.employerID_nd # error, undeletable
        b.employerID_nd = '324ds343' # OK, not readonly

        with self.assertRaises(AttributeError):
            b.securityID_rond = '32342234' # error, readonly
        with self.assertRaises(AttributeError):
            del b.securityID_rond # error, not deletable

        with self.assertRaises(AttributeError):
            b.employer = 'Facebook' # error, it's value was 'Shady Company' which prevents overwrite and delete.
        with self.assertRaises(AttributeError):
            del b.employer # error, it's value was 'Shady Company' which prevents overwrite and delete.
        
        # normal property: setable, getable and deletable
        assert b.current_location_p == 'Some street'
        b.current_location_p = 'Some other street'
        assert b.current_location_p == 'Some other street'
        del b.current_location_p # this will delete the internal variable associated with the property
        assert b.current_location_p == 'Some street' # default value still exists, because the propery itself can not
        # be deleted through instance object and the property had a default value 'Some street'

        # this is a normal attribute not property (as defined)
        b.current_status = 'OK'
        with self.assertRaises(AttributeError):
            B.Props.Defaults.current_status



    def test_PropMixin_Props(self):
        class B(PropMixin):
            name = 'John Doe'
            employer = Prop('Google') # normal Prop property
        
        assert B.Props.Defaults.employer == 'Google'
        
        with self.assertRaises(AttributeError):
            B.Props = 4 # Props is readonly
        with self.assertRaises(AttributeError):
            del B.Props # Props is undeletable
        
        with self.assertRaises(AttributeError):
            B.Props.Defaults = 4 # Props.Defaults is readonly
        with self.assertRaises(AttributeError):
            del B.Props.Defaults # Props.Defaults is undeletable
        
        with self.assertRaises(AttributeError):
            B.Props.Keys = 4 # Props.Keys is readonly
        with self.assertRaises(AttributeError):
            del B.Props.Keys # Props.Keys is undeletable
        
        with self.assertRaises(AttributeError):
            B.Props.Ivan = 4 # Props.Ivan is readonly
        with self.assertRaises(AttributeError):
            del B.Props.Ivan # Props.Ivan is undeletable
        
        with self.assertRaises(AttributeError):
            B.Props.Conf = 4 # Props.Conf is readonly
        with self.assertRaises(AttributeError):
            del B.Props.Conf # Props.Conf is undeletable
        
        # _Props_ is the internal variable for Props
        assert B._Props_ is B.Props
        with self.assertRaises(AttributeError):
            B._Props_ = 3 # still readonly :D
        with self.assertRaises(AttributeError):
            del B._Props_ # still undeletable :D
        
        # _Keys_Internal_Var and _Keys are internal vars for Props.Keys
        with self.assertRaises(AttributeError):
            B.Props._Keys_Internal_Var = 4 # readonly
        with self.assertRaises(AttributeError):
            B.Props._Keys = 4 # readonly
        
        # _Defaults_Internal_Var and _Defaults are internal vars for Props.Defaults
        with self.assertRaises(AttributeError):
            B.Props._Defaults_Internal_Var = 4 # readonly
        with self.assertRaises(AttributeError):
            B.Props._Defaults = 4 # readonly
        
        # _Ivan_Internal_Var and _Ivan are internal vars for Props.Ivan
        with self.assertRaises(AttributeError):
            B.Props._Ivan_Internal_Var = 4 # readonly
        with self.assertRaises(AttributeError):
            B.Props._Ivan = 4 # readonly
        
        # _Conf_Internal_Var and _Conf are internal vars for Props.Conf
        with self.assertRaises(AttributeError):
            B.Props._Conf_Internal_Var = 4 # readonly
        with self.assertRaises(AttributeError):
            B.Props._Conf = 4 # readonly
        
        with self.assertRaises(AttributeError):
            B.Props.D = 3
        
        with self.assertRaises(AttributeError):
            B.Props._Keys.employer = 4
        
        with self.assertRaises(AttributeError):
            B.Props.Keys.employer = 4
        
        
        del B.Props._Keys.employer # Direct deletion is always possible
        
        with self.assertRaises(AttributeError):
            del B.Props._Keys.employer # was deleted by hack
        
        # now that it was deleted, it can be reset:
        B.Props._Keys.employer = 4
        assert B.Props._Keys.employer == 4


    def test_PropMixin_Inheritance(self):
        
        class B(PropMixin):
            name = 'John Doe'
            employer = Prop('Google') # normal Prop property

        class C(B):
            current_status = Prop('OK')

        class D(C):
            """Some class """
            name = Prop("Overwritten")

        d = D()
        D.myname = Prop('Myname')
        assert D.Props.Defaults.name == "Overwritten"
        with self.assertRaises(AttributeError):
            D.Props.Defaults.current_status # Props for class C is  not accessible through class D

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
        assert B.Props.Conf.ceo.is_readonly_for_class() == True

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
