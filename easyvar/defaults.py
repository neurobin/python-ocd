"""Default values for various objects
"""

from easyvar.types import VoidType


def nomodify():
    """A modifier that does not modify the value"""
    return value

def always_valid():
    """A validator that always says 'Valid'"""
    return True


class VarConfig():
    """Abstract base class to be implemented inside classes that need automatic property conversion.

    To make use of this, one must define a class named 'VarConf' that inherits from this
    `VarConfig` class and implements the `get_conf` method. This method should either return
    a `Prop` object (convert to property) or `None` (no conversion).
    """

    def get_conf(self, name, value):
        """This method will be called on each property to get the property configuration.

        It must return a `Prop` object or `None` for the particular property name.
        
        Must be implemented in subclass.

        Args:
            name (str): name of the property
            value (any): Value of the property

        Returns:
            Either `None` (if not to be converted) or `Prop` object if needs to be converted to property.

        """
        raise NotImplementedError("Method 'get_conf' must be implemented in class %s" % (self.__class__.__name__,))
        # return None # this attribute is not to be property converted
        # return Prop() # convert to property according to Prop()
