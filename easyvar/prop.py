"""This module provides functionality related to property, like automatic property creation.

* Provides some functions to make getter and setter functions for various purposes.
* Provides Mixin classes to automatically create properties (with default values if given).
"""
import inspect
from abc import ABCMeta
from pprint import pformat
from copy import deepcopy

from .defaults import Void
from .mapattr import MapAttr


def make_fget(name, var_name, default=Void):
    """Return a function compatible with `property()` function `fget` parameter
    
    Args:
        name (str): name of the property
        var_name (str): internal variable name
        default (any, optional): Default value. Defaults to Void.
    
    Raises:
        AttributeError: when fails to get the attribute
    
    Returns:
        function: A getter function
    """
    def fget(self):
        v = getattr(self, var_name, default)
        if v is Void:
            raise AttributeError("Attribute '%s' exists but it is not set yet and it does not have a default value." % (name,))
        return v
    return fget

def make_fget_const(name, v):
    """Make a getter for `property()` function `fget` param that returns a constant value.
    
    Args:
        name (str): name of the property
        v (any): the constant value of the property
    
    Raises:
        AttributeError: when fails to get the attribute
    
    Returns:
        function: A getter function
    """
    def fget(self):
        if v is Void:
            raise AttributeError("The value of this attribute '%s' is inaccessible or non-existent. Internal reference may exist but hidden." % (name,))
        return v
    return fget

def make_fset(name, var_name):
    """Make a setter for `property()`'s `fset` param for property name and internal variable name
    
    Args:
        name (str): property name
        var_name (str): internal variable name
    
    Returns:
        function: A setter function
    """
    def fset(self, value):
        setattr(self, var_name, value)
    return fset

def make_nofset(name):
    """Make a setter for `property()`'s `fset` param that raises `AttributeError`
    
    Args:
        name (str): property name
    
    Raises:
        AttributeError: always raises exception
    
    Returns:
        function: A setter function
    """
    def fset(self, value):
        raise AttributeError("'%s' is a readonly property" % (name,))
    return fset

def make_fdel(name, var_name=None):
    """Make a deleter for `property()`'s `fdel` param
    
    Args:
        name (str): property name
        var_name (str, optional): internal variable name. Defaults to `None`.
    
    Returns:
        function: A deleter function
    """
    def fdel(self):
        delattr(self, name)
        if var_name:
            delattr(self, var_name)
    return fdel

def make_nofdel(name):
    """Make a deleter for `property()`'s `fdel` param that raises `AttributeError`
    
    Args:
        name (str): property name
    
    Raises:
        AttributeError: always raises exception
    
    Returns:
        function: A deleter function
    """
    def fdel(self):
        raise AttributeError("Attribute '%s' is not deletable")
    return fdel


class Prop():
    """A class that stores configuration for a specific property"""
    def __init__(self, value=Void,
                 readonly_weak=False,
                 readonly=False,    # whether all values of this property should be readonly
                 var_name_prefix='_',
                 var_name_suffix='',
                 deletable=True):
        """Prop constructor that creates property config.
        
        Args:
            value (any, optional): Default value for the property.
            readonly_weak (bool, optional): Property will be readonly but changeable through internal variable. Defaults to False.
            readonly (bool, optional): Unchangeable property. Mutable values can still be changed inplace. Defaults to False.
            var_name_prefix (str, optional): Prefix to add to create internal variable. Defaults to '_'.
            var_name_suffix (str, optional): Suffix to add to create internal variable. Defaults to ''.
            deletable (bool, optional): Whether the property should be deletable. Defaults to True.
        
        Raises:
            ValueError: When an argument fails validation check.
        """
        self.readonly = readonly
        self.readonly_weak = readonly_weak
        self.deletable = deletable
        self.value = value      # Temporary attribute

        self.var_name_prefix = var_name_prefix
        if not isinstance(self.var_name_prefix, str) or not self.var_name_prefix:
            raise ValueError("var_name_prefix needs to be a non empty string")
        elif self.var_name_prefix.startswith('__'):
            raise ValueError("Leading double underscore is not allowed in var_name_prefix")
        elif not self.var_name_prefix.startswith('_'):
            raise ValueError("var_name_prefix must start with a single underscore")

        self.var_name_suffix = var_name_suffix
        if not isinstance(self.var_name_suffix, str):
            raise ValueError("var_name_suffix needs to be a string")
        elif self.var_name_suffix.endswith('__'):
            raise ValueError("Trailing double underscore is not allowed in var_name_suffix")



class PropConfig():
    """Abstract base class to be implemented inside classes that need automatic property conversion.

    To make use of this, one must define a class named 'PropConfig' that inherits from this
    `PropConfig` class and implements the `get_config` method. This method should either return
    a `Prop` object (convert to property) or `None` (no conversion).
    
    Raises:
        NotImplementedError: `get_config` method must be implemented
    """

    def get_config(self, name, value):
        """This method will be called on each property to get the property configuration.

        It must return a `Prop` object or `None` for the particular property name.
        
        Must be implemented in subclass.

        Args:
            name (str): name of the property
            value (any): Value of the property

        Returns:
            Either `None` (if not to be converted) or `Prop` object if needs to be converted to property.

        """
        raise NotImplementedError("Method 'get_config' must be implemented in class %s" % (self.__class__.__name__,))
        # return None # this attribute is not to be property converted
        # return Prop() # convert to property according to Prop()


class PropMeta(ABCMeta):
    """Metaclass for `PropMixin` that will modify the subclasses to define properties automatically.
    
    Do note that this is a metaclass, you don't need to inherit it, rather inherit the `PropMixin` class.
    The `Props` attribute of this class will be available through your class name. For example:

    ```python
    class MyClass(PropMixin):
        my_property = Prop('Building A/2')
    
    default_value = MyClass.Props.Defaults.my_property
    ```
    """
    class __Props():
        """Store information of class properties"""
        class _Keys(MapAttr): pass
        class _Defaults(MapAttr): pass
        class _Conf(MapAttr): pass
        class _Ivan(MapAttr): pass
        
        Keys = property(fget=make_fget_const('Keys', _Keys()),
                        fset=make_nofset('Keys'),
                        fdel=make_nofdel('Keys'),
                        doc='Stores the names of properties accessible by attribute with same name. See details in doc for `Props`.')
        Defaults = property(fget=make_fget_const('Defaults', _Defaults()),
                            fset=make_nofset('Defaults'),
                            fdel=make_nofdel('Defaults'),
                            doc='Stores the default values of the properties accessible by attribute with same name. See details in doc for `Props`.')
        Conf = property(fget=make_fget_const('Conf', _Conf()),
                        fset=make_nofset('Conf'),
                        fdel=make_nofdel('Conf'),
                        doc='Stores configuration of the properties accessible by attribute with same name. See details in doc for `Props`.')

        Ivan = property(fget=make_fget_const('Ivan', _Ivan()),
                        fset=make_nofset('Ivan'),
                        fdel=make_nofdel('Ivan'),
                        doc='Stores the internal variable names of the properties accessible by attribute with same name. See details in doc for `Props`.')
        
        # Convenience aliases
        K = Keys
        D = Defaults
        C = Conf
        I = Ivan
    
    Props = property(fget=make_fget_const('Props', __Props()),
                     fset=make_nofset('Props'),
                     fdel=make_nofdel('Props'),
                     doc="""This attribute contains some other attributes to provide more information about properties.

                     Keys
                     ====
                     Contains the name of the properties accessible as attributes.
                     For example, an attribute named 'author_name' can be accessed as:
                     `Props.Keys.author_name`. It will return the name of the attribute as string: 'author_name'
                     
                     Defaults
                     ========
                     Stores the default values of properties.

                     `Props.Defaults.author_name` will return the default value of `author_name` attribute.

                     Conf
                     ====
                     Stores the configuration of property.

                     `Props.Conf.author_name` will return a `Prop` object.

                     Ivan
                     ====
                     Stores the internal variable name of property.

                     `Props.Ivan.author_name will` return the name of the internal variable for `author_name` property as `str`.
                     """)


    def __new__(mcs, class_name, bases, attrs):
        reserved_aatrs = ['Props',]
        for K in reserved_aatrs:
            if K in attrs:
                raise AttributeError("'%s' is a reserved attribute for class '%s' defined in '%r'. \
                    Please do not redefine it." % (K, class_name, mcs,))
        cls = super(PropMeta, mcs).__new__(mcs, class_name, bases, attrs)
        dir_cls = dir(cls)

        prop_config = Void
        prop_config_class_name = 'PropConfig'
        if prop_config_class_name in dir_cls:
            PropConfigClass = getattr(cls, prop_config_class_name)
            if inspect.isclass(PropConfigClass):
                prop_config = PropConfigClass()
            else:
                raise TypeError("'%s' in class '%s' needs to be a *class* that inherits \
                    and implements '%s' class." % (prop_config_class_name, class_name, prop_config_class_name,))

        for n in dir_cls:
            if n.startswith('_'):
                # names starting with _ will not be converted to properties whether they are defined as Prop()
                # This will allow us to define protected Prop() variables inside class for other uses.
                continue
            p = getattr(cls, n)
            val = p

            if prop_config and not isinstance(p, Prop):
                # make it Prop
                p = prop_config.get_config(n, val)

            if isinstance(p, Prop):
                var_name = ''.join([p.var_name_prefix, n, p.var_name_suffix])

                nofset = make_nofset(n)

                if p.deletable:
                    # name nfdel comes from fdel only on name (n)
                    nfdel = make_fdel(n)
                    vfdel = make_fdel(n, var_name)
                else:
                    nfdel = make_nofdel(n)
                    vfdel = nfdel

                if p.value is not Void:
                    val = p.value
                del p.value

                setattr(cls.Props._Conf, n, property(fget=make_fget_const(n, p), fset=nofset, fdel=nfdel))

                setattr(cls.Props._Keys, n, property(fget=make_fget_const(n, n), fset=nofset, fdel=nfdel))

                
                # default value is always readonly
                # it does not make sense to change default value later as it will
                # have no effect because value will act on its own deepcopy version.
                dfset = nofset
                dfget = make_fget_const(n, val)
                dfdel = nfdel
                setattr(cls.Props._Defaults, n, property(fget=dfget, fset=dfset, fdel=dfdel))

                if p.readonly:
                    # constant value, no internal vars
                    fset = dfset
                    fget = dfget
                    fdel = nfdel
                elif p.readonly_weak:
                    # value can not be set through property but internal var
                    # thus value is not constant.
                    fset = nofset
                    fget = make_fget(n, var_name, deepcopy(val))
                    fdel = vfdel
                    # save the internal var name in Ivan
                    setattr(cls.Props._Ivan, n, property(fget=make_fget_const(n, var_name), fset=nofset, fdel=nfdel))
                else:
                    fset = make_fset(n, var_name)
                    fget = make_fget(n, var_name, deepcopy(val))
                    fdel = vfdel
                    # save the internal var name in Ivan
                    setattr(cls.Props._Ivan, n, property(fget=make_fget_const(n, var_name), fset=nofset, fdel=nfdel))

                # delattr(cls, n) # may not be needed
                setattr(cls, n, property(fget=fget, fset=fset, fdel=fdel))

        return cls

class PropMixin(metaclass=PropMeta):
    """A base class that modifies the subclasses to define properties automatically.
    
    Each defined property will also have their configurations/metadata and default values saved in
    a special property named `Props` in the subclass.

    An example:

    ```python
    class MyClass(PropMixin):
        class PropConfig():
            def get_config(self, name, value):
                return Prop(readonly=True)
        
        author_name = 'Jahidul Hamid'
        version = 'Some version'
        etc = 'etc...'
    ```

    The above class's attributes will be converted to readonly properties. Thus, when you do:

    ```python
    m = MyClass()
    m.author_name = 'John Doe' # throws AttributeError
    ```

    It will throw `AttributeError` saying that you are trying to modify a readonly property.
    Thus the objects of this class can only access the property and not modify it.

    However, mutable values can still be changed inplace :D.

    You can not change the value of the property like `m._author_name` as no internal
    variable is created when `readonly=True`. If you need internal variables, pass
    `readonly_weak=True` which will let you change the values through internal variables.
    By the way, all mingling with protected variables like `m._author_name`
    should be done inside class method definitions. The name of the internal variable
    `_author_name` will be made up by prefixing the property name
    with a single underscore. You can set up custom prefix and suffix (check the options
    provided by `Prop`)

    Other than creating the property it does several other things. It creates a special
    property named `Props` in your class (`MyClass`) and stores some information and default
    values in it.

    Mixed type of properties
    ========================

    In above, all class attributes were being converted to **readonly** property. Now let's
    see how we can have mixed types of properties:

    ```python
    class MyClass(PropMixin):
        class PropConfig():
            def get_config(self, name, value):
                if name.lower().startswith('ro_'):
                    # variables ending with ro_ (case insensitive) will become readonly property
                    return Prop(readonly=True)
                elif name.lower().startswith('wro_'):
                    # vars ending with wro_ (case insensitive) will become properties whose
                    # values can be changed through internal variables (weak readonly).
                    return Prop(readonly_weak=False)
                elif name.lower().startswith('ndel_'):
                    # These properties won't be deletable
                    return Prop(deletable=False)
                elif: name.lower().startswith('p_'):
                    # make these normal properties whose values can be changed
                    return Prop()
                else:
                    # other properties that do not match the above criteria
                    # won't be converted to properties.
                    return None
        
        # These won't be converted to properties
        author_name = 'John Doe'
        version = 'Some version'
        etc = 'etc...'
        
        # These will become readonly properties
        ro_author_name = 'John Doe'
        ro_version = 'Some version'
        ro_etc = 'etc...'
        
        # weak readonly properties that can be changed with internal vars
        wro_author_name = 'John Doe'
        wro_version = 'Some version'
        wro_etc = 'etc...'
        
        # Non deletable properties
        ndel_author = 'John Doe'
        ndel_version = 'Some version'
        ndel_etc = 'etc...'
        
        # Normal properties
        p_author_name = 'John Doe'
        p_version = 'Some version'
        p_etc = 'etc...'
    ```


    A special class attribute `Props`
    =================================

    `Props` attribute provides some information about the properties. The following table should depict
    what information can be accessed by `Props`.

    Attribute  | Short | Details
    ---------- | ----- | -------
    `Keys`     | `K`     | `MyClass.Props.Keys.author_name` will return 'author_name' (the name of the property)
    `Defaults` | `D`     | `MyClass.Props.Defaults.author_name` will return 'John Doe' (the default value)
    `Conf`     | `M`     | `MyClass.Props.Conf.author_name` will return a `Prop` object for `author_name`
    `Ivan`     | `I`     | `MyClass.Props.Ivan.author_name` will return '_author_name' (internal variable name)

    Note
    ====

    * We do not allow variables starting with an underscores to be converted to property.
    * Variables with leading undersocore can store `Prop` class objects without getting converted to property.
    
    """
    pass
