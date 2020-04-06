
import unittest

from easyvar.prop import Prop, PropMixin
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
            print("b_internal: ", B.Props.Ivan.b)
            B.Props.Ivan.b # readonly, so no internal variable
        
        
        B.Props.Ivan.d # weak readonly, so there is an internal variable

        b.c.append(4)
        assert b.c == [1,2,3,4]
    
    def test_PropMixin_VarConf_Validity(self):
        with self.assertRaises(TypeError):
            class B(PropMixin):
                class VarConf(): # get_conf not implemented
                    pass
        with self.assertRaises(TypeError):
            class B(PropMixin):
                VarConf = 4 # VarConf is a class
        
        with self.assertRaises(TypeError):
            class B(PropMixin):
                class VarConf():
                    def get_conf(): # needs to accept name and value pair
                        pass
            

        class B(PropMixin):
            class VarConf():
                @staticmethod
                def get_conf(n, v):
                    return None

        class B(PropMixin):
            class VarConf():
                @classmethod
                def get_conf(cls, n, v):
                    return None

        with self.assertRaises(AssertionError):
            class B(PropMixin):
                class VarConf():
                    def get_conf(self, n, v):
                        return True # needs to return None or Prop object
        
        # OK
        class B(PropMixin):
            class VarConf():
                def get_conf(self, n, v):
                    return None
        
        # OK
        class B(PropMixin):
            class VarConf():
                def get_conf(self, n, v):
                    return Prop()
    
    def test_PropMixin_VarConf_Uses(self):
        class B(PropMixin):
            class VarConf():
                def get_conf(self, n, v):
                    return Prop(readonly=True)

            name = 'John Doe' # readonly
            employer = Prop('Google') # not readonly
        
        b = B()
        with self.assertRaises(AttributeError):
            b.name = 'Me' # Fail
        
        b.employer = 'Facebook' # OK


        class B(PropMixin):
            class VarConf():
                def get_conf(self, n, v):
                    if n.endswith('_ro'):
                        return Prop(readonly=True)
                    elif n.endswith('_wro'):
                        return Prop(readonly_weak=True)
                    elif n.endswith('_nd'):
                        return Prop(deletable=False)
                    elif n.endswith('_rond'):
                        return Prop(deletable=False, readonly=True)
                    elif v == 'Shady Company': # attribute with value 'Shady Company' will be readonly and undeletable
                        return Prop(deletable=False, readonly=True)
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
        del b.current_location_p # this will delete the property with all of it's config
        print(b.current_location_p)
        with self.assertRaises(AttributeError):
            b.current_location_p # no such property anymore
        with self.assertRaises(AttributeError):
            B.Props.Keys.current_location_p # this has also been deleted
        with self.assertRaises(AttributeError):
            B.Props.Defaults.current_location_p # deleted as well
        with self.assertRaises(AttributeError):
            B.Props.Ivan.current_location_p # deleted
        with self.assertRaises(AttributeError):
            B.Props.Conf.current_location_p # deleted
        
        # Now if you create an attribute with the same name of the deleted property, it will be
        # a completely new thing
        b.current_location_p = 2 # it's just an attribute, not a property anymore
        with self.assertRaises(AttributeError):
            B.Props.Conf.current_location_p # it does not exist anymore.
        # Once you delete a Prop() property you can not get it back again.
        # If you just want to disable the property temporarily, you can do it
        # in the following way:
        b.some_var = Void # easyvar.Void, this will make it non existent while existing
        with self.assertRaises(AttributeError):
            b.some_var
        # But the property exists:
        assert B.Props.Defaults.some_var == 34
        b.some_var = 12 # still a property

        # this is a normal attribute not property (as defined)
        b.current_status = 'OK'
        with self.assertRaises(AttributeError):
            B.Props.Defaults.current_status



    def test_PropMixin_Props(self):
        class B(PropMixin):
            name = 'John Doe'
            employer = Prop('Google') # normal Prop property
        
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


    def test_PropMixin_Inheritance(self):
        
        class B(PropMixin):
            name = 'John Doe'
            employer = Prop('Google') # normal Prop property

        class C(B):
            current_status = Prop('OK')

        class D(C):
            name = Prop("Overwritten")

        d = D()
        D.myname = Prop('Myname')
        assert D.Props.Defaults.name == "Overwritten"






if __name__ == '__main__':
    unittest.main(verbosity=2)
