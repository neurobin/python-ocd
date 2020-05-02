
import unittest
from easyvar import decorators as dcr
import inspect

class Test_decorators(unittest.TestCase):
    def setUp(self):
        # init
        pass

    def tearDown(self):
        # destruct
        pass

    def test_deprecated(self):
        me = self.tearDown
        @dcr.deprecate(by='fun2', ver_cur='1.3', ver_dep='1.3', ver_end='1.3')
        def fun(a, b=3):
            """[summary]

            [extended_summary]

            Args:
                self ([type]): [description]
                b (int, optional): [description]. Defaults to 3.
            """
            print(a, b)
            pass

        fun(2, 3)
        # print(inspect.getsource(fun))
        # var = 3
        # @dcr.deprecated
        # var

        # class M():
        #     x = Descriptor('x', 5)
        # print(str(M.x))





if __name__ == '__main__':
    unittest.main(verbosity=2)
