"""Utility functions.
"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.1'


import inspect
import copy
import uuid


def copy_class(cls):
    """Return a shallow copy version of class `cls`

    Args:
        cls (class): class that needs to be copied.
    """
    class_name = '_%s_%s' % (cls.__name__, str(uuid.uuid4()).replace('-', '_'))
    new_bases = cls.__bases__
    new_attrs = dict(cls.__dict__)
    return type(class_name, new_bases, new_attrs)

def copy_shallow(obj):
    """Return a shallow copy version of obj where obj can be a class.

    Args:
        obj (any): object that needs to be copied.
    """
    if inspect.isclass(obj):
        return copy_class(obj)
    else:
        return copy.copy(obj)

def copy_semideep(obj):
    """Return a deep copy version of obj by calling copy.deepcopy if
    obj is not a class, otherwise return a shallow copy for class
    itself.

    Args:
        obj (any): object that needs to be copied.
    """
    if inspect.isclass(obj):
        return copy_class(obj)
    else:
        return copy.deepcopy(obj)
