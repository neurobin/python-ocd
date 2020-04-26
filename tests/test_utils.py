
import unittest

from easyvar import utils

class Test_utils(unittest.TestCase):
    def setUp(self):
        # init
        pass

    def tearDown(self):
        # destruct
        pass

    def test_semideepcopy(self):
        class B(object): pass
        b = B()

        B0 = utils.semideepcopy(B)
        b0 = utils.semideepcopy(b)

        B.a = 3
        B0.a = 4
        self.assertTrue(B.a == 3)

        b.b = 4
        b0.b = 5
        self.assertTrue(b.b == 4)

        self.assertTrue(b is not b0)
        self.assertTrue(B is not B0)

    def test_shallowcopy(self):
        class B(object): pass
        b = B()

        B0 = utils.shallowcopy(B)
        b0 = utils.shallowcopy(b)

        B.a = 3
        B0.a = 4
        self.assertTrue(B.a == 3)

        b.b = 4
        b0.b = 5
        self.assertTrue(b.b == 4)

        self.assertTrue(b is not b0)
        self.assertTrue(B is not B0)



if __name__ == '__main__':
    unittest.main(verbosity=2)
