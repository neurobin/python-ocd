
import unittest
from ocd.deprecate import deprecate, raiseUnsupportedWarning
from ocd.warnings import DeprecatedWarning, UnsupportedWarning
import inspect

class Test_decorators(unittest.TestCase):
    def setUp(self):
        # init
        pass

    def tearDown(self):
        # destruct
        pass

    @raiseUnsupportedWarning
    def test_deprecated(self):
        @deprecate(by='fun2', ver_cur='1.3', ver_dep='1.3', ver_end='1.4')
        def fun(a, b=3):
            pass

        with self.assertWarns(DeprecatedWarning):
            fun(2, 3)
        with self.assertWarns(DeprecatedWarning):
            fun(2, 3)
        with self.assertWarns(DeprecatedWarning):
            fun(2, 3)


        with self.assertRaises(ValueError):
            @deprecate(ver_end='1.0')
            def fun2(a, b=3):pass
            fun2(4)

        @deprecate(me='fun3', by='fun2', ver_cur='1.3', ver_dep='1.3', ver_end='1.3')
        def fun3(a, b=3):
            pass

        with self.assertRaises(UnsupportedWarning):
            fun3(2)


        @deprecate(by='fun2', ver_cur='1.3', ver_dep='1.3', ver_end='1.5', msg_dep="dep")
        def fun4(a, b=3):
            pass
        fun4(3)

    def test_no_raise_UnsupportedWarning(self):

        @deprecate(me='fun3', by='fun2', ver_cur='1.3', ver_dep='1.3', ver_end='1.3')
        def fun3(a, b=3):
            pass
        fun3(2)





if __name__ == '__main__':
    unittest.main(verbosity=2)
