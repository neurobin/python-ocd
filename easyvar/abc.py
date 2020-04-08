


class VarConf():
    """A base class that must be inherited by `VarConf` classes in subclasses of `PropMixin`.
    
    The method `get_conf` must be implemented in your `VarConf` class.

    If you want automatic property configuration, create a class named `VarConf` in your
    `PropMixin` subclass and make your `VarConf` class inherit from `easyvar.abc.VarConf`
    or a default `VarConf` class from `easyvar.defaults` and implement the `get_conf`
    method to either return a `Prop` object for property conversion to happen for 
    the corresponding attribute name or return `None` if no conversion is desired.
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
        raise NotImplementedError("`VarConf` class must define a method `get_conf` that returns `Prop` object or `None`. See `easyvar.abc.VarConf`")