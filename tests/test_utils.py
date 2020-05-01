
import unittest

from easyvar import utils

class Test_utils(unittest.TestCase):
    def setUp(self):
        # init
        pass

    def tearDown(self):
        # destruct
        pass

    def test_copy_semideep(self):
        class B(object): pass
        b = B()

        B0 = utils.copy_semideep(B)
        b0 = utils.copy_semideep(b)

        B.a = 3
        B0.a = 4
        self.assertTrue(B.a == 3)

        b.b = 4
        b0.b = 5
        self.assertTrue(b.b == 4)

        self.assertTrue(b is not b0)
        self.assertTrue(B is not B0)

    def test_copy_shallow(self):
        class B(object): pass
        b = B()

        B0 = utils.copy_shallow(B)
        b0 = utils.copy_shallow(b)

        B.a = 3
        B0.a = 4
        self.assertTrue(B.a == 3)

        b.b = 4
        b0.b = 5
        self.assertTrue(b.b == 4)

        self.assertTrue(b is not b0)
        self.assertTrue(B is not B0)

    def test_copy_class(self):
        class B():
            a = 3
        C = utils.copy_class(B)
        self.assertTrue(C is not B)
        with self.assertRaises(AssertionError):
            self.assertTrue(C.a is not B.a) # class copy is shallow
        # and so:
        self.assertTrue(C.a is B.a)

        B.b = 4
        C.b = 5

        self.assertTrue(B.b == 4)
        self.assertTrue(C.b == 5)

        # lets' make sure the standard copy
        # still does not support class copy
        import copy
        D = copy.copy(B)
        E = copy.deepcopy(B)
        self.assertTrue(D is B)
        self.assertTrue(E is B)



if __name__ == '__main__':
    unittest.main(verbosity=2)
