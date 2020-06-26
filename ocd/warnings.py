"""Warnings.
"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.1'



class UnsupportedWarning(DeprecationWarning):
    """Base class for warnings about unsupported features."""
    def __init__(self, msg):
        self.message = msg
        super(UnsupportedWarning, self).__init__()

    def __str__(self):
        msg = self.message
        return msg


class DeprecatedWarning(DeprecationWarning):
    def __init__(self, msg):
        self.message = msg
        super(DeprecatedWarning, self).__init__()

    def __str__(self):
        msg = self.message
        return msg
