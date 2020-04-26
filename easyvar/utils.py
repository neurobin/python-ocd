"""Utility functions
"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.1'


import inspect
import copy
import uuid


def shallowcopy(obj):
    """Return a shallow copy version of obj where obj can be a class.

    Args:
        obj (any): object that needs to be copied.
    """
    if inspect.isclass(obj):
        class_name = 'NewClass_' + str(uuid.uuid4()).replace('-', '_')
        new_bases = obj.__bases__
        new_attrs = dict(obj.__dict__)
        return type(class_name, new_bases, new_attrs)
    else:
        return copy.copy(obj)


def semideepcopy(obj):
    """Return a deep copy version of obj if obj is not a class,
    otherwise return a shallow copy for class itself.

    Args:
        obj (any): object that needs to be copied.
    """
    if inspect.isclass(obj):
        class_name = 'NewClass_' + str(uuid.uuid4()).replace('-', '_')
        new_bases = obj.__bases__
        new_attrs = dict(obj.__dict__)
        return type(class_name, new_bases, new_attrs)
    else:
        return copy.deepcopy(obj)
