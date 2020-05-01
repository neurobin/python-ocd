"""Our decorators.

"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.1'


import inspect
import traceback
import warnings
import functools
from packaging import version

def deprecate(_func=None, *,
              me='',
              by='',
              ver_cur='',
              ver_dep='',
              ver_end='',
              msg_format="`%s` is deprecated by `%s` from version `%s` and "
                         "will be removed in version `%s`. Current version:"
                         " `%s`"
              ):
    _ver_cur = version.parse(ver_cur)
    _ver_dep = version.parse(ver_dep)
    _ver_end = version.parse(ver_end)
    def deprecator(func):
        _me = me
        if not _me:
            _me = repr(func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if _ver_cur >= _ver_dep:
                warnings.simplefilter('default', DeprecationWarning)
                warnings.warn(msg_format % (_me, by, ver_dep, ver_end, ver_cur),
                            category=DeprecationWarning,
                            stacklevel=2)
            elif _ver_cur >= _ver_end:
                raise NotImplementedError
            return func(*args, **kwargs)
        return wrapper
    if _func is None:
        return deprecator(_func)
    return deprecator
