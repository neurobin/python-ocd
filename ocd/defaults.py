"""Default classes and methods
"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.5'


from ocd import abc
from ocd import prop


def nomodify(value):
    """A modifier that does not modify the value."""
    return value

def always_valid(value):
    """A validator that always says 'Valid'."""
    return True


class VarConfNone(abc.VarConf):
    """A `VarConf` class that implements `get_conf` method that always
    returns `None`

    This is a dummy `VarConf` that makes no changes and does no
    automatic property conversion.
    """

    def get_conf(self, name, value):
        """Return `None` i.e no property conversion will take place
        """
        return None


class VarConfAll(abc.VarConf):
    """A `VarConf` class that implements `get_conf` method that always
    returns a `Prop` object with defaults.

    This `VarConf` will convert all class attributes that do not
    start with an undersocore '_' to properties with default
    configuration `Prop()`.

    To see the defaults, see class `ocd.prop.Prop`
    """

    def get_conf(self, name, value):
        """Return `Prop()` i.e all public attributes will become
        properties.
        """
        return prop.Prop()


class VarConfAllUnro(abc.VarConf):
    """A `VarConf` class that implements `get_conf` method that always
    returns a `Prop` object with readonly=True and undead=True.

    This `VarConf` will convert all class attributes that do not
    start with an undersocore '_' to properties that can not be deleted
    or changed.
    """

    def get_conf(self, name, value):
        """Return `Prop(readonly=True, undead=True)` i.e all public
        attributes will become readonly, undead properties.
        """
        return prop.Prop(readonly=True, undead=True)
