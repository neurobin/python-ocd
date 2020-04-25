"""Tests for the package's __init__.py
"""
import unittest


class Test_Package(unittest.TestCase):
    def setUp(self):
        # init
        pass
    
    def tearDown(self):
        # destruct
        pass
    
    def test_imports(self):
        from easyvar import Void



if __name__ == '__main__':
    unittest.main(verbosity=2)
