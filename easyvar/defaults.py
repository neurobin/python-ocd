"""Default values for various objects
"""

from easyvar.types import VoidType


def nomodify():
    """A modifier that does not modify the value"""
    return value

def always_valid():
    """A validator that always says 'Valid'"""
    return True


class VarConf():
    """A default `VarConf` class that implements `get_conf` method that always returns `None`
    
    This is a dummy `VarConf` that makes no changes.

    If you want automatic property configuration, override this class in subclasses of `PropMixin`
    and implement the `get_conf` method to either return a `Prop` object for property
    conversion to happen for the corresponding attribute name or return `None` if no
    conversion is desired.
    """

    def get_conf(self, name, value):
        """This method will be called on each property to get the property configuration.

        It must return a `Prop` object or `None` for the particular property name.

        Args:
            name (str): name of the property
            value (any): Value of the property

        Returns:
            Either `None` (if not to be converted) or `Prop` object if needs to be converted to property.

        """
        return None # this attribute is not to be property converted
