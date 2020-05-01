
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
        dcr.deprecate()
        @dcr.deprecate(by='Someone')
        def fun(a, b=3):
            """[summary]

            [extended_summary]

            Args:
                self ([type]): [description]
                b (int, optional): [description]. Defaults to 3.
            """
            print(a, b)

        fun(2, 3)
        # print(inspect.getsource(fun))
        # var = 3
        # @dcr.deprecated
        # var




if __name__ == '__main__':
    unittest.main(verbosity=2)
