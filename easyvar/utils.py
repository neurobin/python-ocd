# -*- coding: utf-8 -*-

"""Utility functions

-------------------------------------------------------------------
Copyright: Md. Jahidul Hamid <jahidulhamid@yahoo.com>

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
-------------------------------------------------------------------
"""

import inspect
import copy


def deepcopy(obj):
    """Return a deepcopy version of obj. obj can be a class as well as class instance.

    Args:
        obj (any): object that needs to be deepcopied.
    """
    if inspect.isclass(obj):
        return type('new_class', obj.__bases__, dict(obj.__dict__))
    else:
        return copy.deepcopy(obj)
