"""This module provides functionality related to property, like automatic property creation.

* Provides some functions to make getter and setter functions for various purposes.
* Provides Mixin classes to automatically create properties (with default values if given).
"""
import inspect
from abc import ABCMeta
from pprint import pformat
from copy import deepcopy

from easyvar import Void
from easyvar.mapattr import MapAttr
from easyvar import defaults


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
            raise AttributeError("Attribute '%s' exists but it is not set yet and it "\
                "does not have a default value." % (name,))
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
            raise AttributeError("The value of this attribute '%s' is inaccessible or non-existent. "\
                "Internal reference may exist but hidden." % (name,))
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
        var_name (str): internal variable name.
    
    Returns:
        function: A deleter function
    """
    def fdel(self):
        if var_name:
            delattr(self, var_name)
        else:
            raise AttributeError("Property '%s' belongs to the class '%r'. It can not be deleted through a class object." % (name, self.__class__,))
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
        raise AttributeError("Attribute '%s' is not deletable" % (name,))
    return fdel


class Prop():
    """A class that stores configuration for a specific property"""
    def __init__(self, value=Void,
                 readonly_weak=False,
                 readonly=False,    # whether all values of this property should be readonly
                 readonly_for_class=True,
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

        if self.readonly and self.readonly_weak:
            raise ValueError("readonly and readonly_weak can not be True at the same time. It's either weak or strong not both.")

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


class _Props():
    """Store information of class properties"""

    def __init__(self):
        class Keys(MapAttr): pass
        class Defaults(MapAttr): pass
        class Conf(MapAttr): pass
        class Ivan(MapAttr): pass
        self._Keys_Internal_Var = Keys()
        self._Defaults_Internal_Var = Defaults()
        self._Conf_Internal_Var = Conf()
        self._Ivan_Internal_Var = Ivan()
        self._Keys_Class = Keys
        self._Defaults_Class = Defaults
        self._Conf_Class = Conf
        self._Ivan_Class = Ivan
    
    # internal class property
    _Keys = property(fget=make_fget('_Keys', '_Keys_Class'), fset=make_nofset('_Keys'), fdel=make_nofdel('_Keys'))
    _Defaults = property(fget=make_fget('_Defaults', '_Defaults_Class'), fset=make_nofset('_Defaults'), fdel=make_nofdel('_Defaults'))
    _Conf = property(fget=make_fget('_Conf', '_Conf_Class'), fset=make_nofset('_Conf'), fdel=make_nofdel('_Conf'))
    _Ivan = property(fget=make_fget('_Ivan', '_Ivan_Class'), fset=make_nofset('_Ivan'), fdel=make_nofdel('_Ivan'))
    
    # class property
    Keys = property(fget=make_fget('Keys', '_Keys_Internal_Var'),
                    fset=make_nofset('Keys'),
                    fdel=make_nofdel('Keys'),
                    doc='Stores the names of properties accessible by attribute with same name. See details in doc for `Props`.')
    Defaults = property(fget=make_fget('Defaults', '_Defaults_Internal_Var'),
                        fset=make_nofset('Defaults'),
                        fdel=make_nofdel('Defaults'),
                        doc='Stores the default values of the properties accessible by attribute with same name. See details in doc for `Props`.')
    Conf = property(fget=make_fget('Conf', '_Conf_Internal_Var'),
                    fset=make_nofset('Conf'),
                    fdel=make_nofdel('Conf'),
                    doc='Stores configuration of the properties accessible by attribute with same name. See details in doc for `Props`.')

    Ivan = property(fget=make_fget('Ivan', '_Ivan_Internal_Var'),
                    fset=make_nofset('Ivan'),
                    fdel=make_nofdel('Ivan'),
                    doc='Stores the internal variable names of the properties accessible by attribute with same name. See details in doc for `Props`.')
    
    # Convenience aliases
    K = Keys
    D = Defaults
    C = Conf
    I = Ivan

    #@staticmethod
    # def _make_fdel_plus_in_Props(name, var_name=None):
    #     """Make a deleter for `property()`'s `fdel` param

    #     This one deletes all additional properties inside Props
        
    #     Args:
    #         name (str): property name
    #         var_name (str, optional): internal variable name. Defaults to `None`.
        
    #     Returns:
    #         function: A deleter function
    #     """
    #     def fdel(self):
    #         # delattr(self.__class__, name)
    #         if var_name:
    #             delattr(self, var_name)
    #         # if this property is deletable, then these would be deletable as well
    #         # delattr(self.__class__.Props.Keys, name)
    #         # delattr(self.__class__.Props.Defaults, name)
    #         # delattr(self.__class__.Props.Conf, name)
    #         # delattr(self.__class__.Props.Ivan, name)
    #     return fdel


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
    # _Props_ = None
    Props = property(fget=make_fget('Props', '_Props_'),
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
    
    def __delattr__(self, name):
        try:
            isProp = getattr(self.Props.Conf, name) # returns None or Prop()
            # if None, then it's not a property
        except:
            isProp = None
        if isProp:
            delattr(self.Props._Keys, name)
            delattr(self.Props._Defaults, name)
            delattr(self.Props._Conf, name)
            if hasattr(self.Props._Ivan, name): # unlike others internal variable is not always available
                delattr(self.Props._Ivan, name)
        super(PropMeta, self).__delattr__(name)
    
    def __setattr__(self, name, value):
        reserved = ['_Props_',]
        if name in reserved:
            raise AttributeError("Attribute name '%s' is reserved by %r." % (name, self.__class__,))
        name_startswith_ = name.startswith('_')
        try:
            prop = getattr(self.Props._Conf, name, None)
        except:
            prop = None
        if isinstance(prop, Prop):
            # trying to overwrite a Prop() definition itself.
            # should we allow it?
            # ... 
            # !!?
            # give option: check an attribute called readonly_for_class is True or not
            if prop.readonly_for_class:
                raise AttributeError("Property '%s' is readonly for class %r" % (name, self.__class__,))
            else:
                pass
        if not name_startswith_ and not isinstance(value, Prop):
            p = self._get_var_conf(name, value)
            if p:
                # returned a Prop, this one needs to be converted to property
                if p.value is Void:
                    p.value = value
                value = p
        
        # now value is OK for final processing
        if not name_startswith_ and isinstance(value, Prop):
            if not hasattr(self, '_Props_'):
                # Props is not set, set it
                # del self._Props_
                super(PropMeta, self).__setattr__('_Props_', _Props())
            print("Creating property '%s' for class '%r'" % (name, self))
            This_Prop, Defaults_Prop, Keys_Prop, Ivan_Prop, Conf_Prop = self._makePropProperties(name, value)
            super(PropMeta, self).__setattr__(name, This_Prop)
            setattr(self.Props._Conf, name, Conf_Prop)
            setattr(self.Props._Defaults, name, Defaults_Prop)
            setattr(self.Props._Keys, name, Keys_Prop)
            if Ivan_Prop: # unlike others internal variable is not always available
                setattr(self.Props._Ivan, name, Ivan_Prop)
        else:
            super(PropMeta, self).__setattr__(name, value)


    def _makePropProperties(self, n, p):
        var_name = ''.join([p.var_name_prefix, n, p.var_name_suffix])

        nofset = make_nofset(n)

        if p.deletable:
            # name nfdel comes from fdel only on name (n)
            nfdel = make_fdel(n)
            main_property_fdel = make_fdel(n, var_name)
        else:
            nfdel = make_nofdel(n)
            main_property_fdel = nfdel

        val = p.value
        del p.value

        dfget = make_fget_const(n, val) # used more than once
        Conf_Prop = property(fget=make_fget_const(n, p), fset=nofset, fdel=nfdel)
        Keys_Prop = property(fget=make_fget_const(n, n), fset=nofset, fdel=nfdel)
        Defaults_Prop = property(fget=dfget, fset=nofset, fdel=nfdel)
        Ivan_Prop = None
        # default value is always readonly ^:
        # it does not make sense to change default value later as it will
        # have no effect because value will act on its own deepcopy version.

        # main property configuration
        if p.readonly:
            # constant value, no internal vars
            fset = nofset
            fget = dfget
            fdel = nfdel
        elif p.readonly_weak:
            # value can not be set through property but internal var
            # thus value is not constant.
            fset = nofset
            fget = make_fget(n, var_name, deepcopy(val))
            fdel = main_property_fdel
            # save the internal var name in Ivan
            Ivan_Prop = property(fget=make_fget_const(n, var_name), fset=nofset, fdel=nfdel)
        else:
            fset = make_fset(n, var_name)
            fget = make_fget(n, var_name, deepcopy(val))
            fdel = main_property_fdel
            # save the internal var name in Ivan
            Ivan_Prop = property(fget=make_fget_const(n, var_name), fset=nofset, fdel=nfdel)

        This_Prop = property(fget=fget, fset=fset, fdel=fdel)
        return This_Prop, Defaults_Prop, Keys_Prop, Ivan_Prop, Conf_Prop
    
    def _get_var_conf(self, name, value):
        p = self.VarConf().get_conf(name, value)
        assert p is None or isinstance(p, Prop), "return value from 'get_conf' in class 'VarConf' "\
                    "inside class '%r' needs to either return None or a Prop object. See example in "\
                    "easyvar.defaults.VarConf" % (self.__class__,)
        return p

    # def __init__(cls, name, bases, attrs):
    #     super(PropMeta, cls).__init__(name, bases, attrs)

    def __new__(mcs, class_name, bases, attrs):
        rserved_attrs = ['Props', '_Props_']
        for K in rserved_attrs:
            if K in attrs:
                raise AttributeError("'%s' is a reserved attribute for class '%s' defined in '%r'. "\
                    "Please do not redefine it." % (K, class_name, mcs,))
        cls = super(PropMeta, mcs).__new__(mcs, class_name, bases, attrs)
        prop_candidates = {}
        non_candidates = ['VarConf']
        for k in attrs:
            if k.startswith('_') or k in non_candidates:
                pass
            else:
                setattr(cls, k, attrs[k])
        # print("")
        # print(repr(cls))
        # for k in prop_candidates:
        #     setattr(cls(), k, prop_candidates[k])
        

        # prop_config = None
        # vcname = 'VarConf'
        # if vcname in dir_cls:
        #     try:
        #         prop_config = cls.VarConf()
        #     except:
        #         raise TypeError("'%s' is reserved by %r and it needs to be defined as a *class* inside class '%s'"\
        #             ", see example in easyvar.defaults.%s" % (vcname, mcs, class_name, vcname,))

        # for n in dir_cls:
        #     if n.startswith('_'):
        #         # names starting with _ will not be converted to properties whether they are defined as Prop()
        #         # This will allow us to define protected Prop() variables inside class for other uses.
        #         continue
        #     p = getattr(cls, n)
        #     val = p

        #     if prop_config and not isinstance(p, Prop):
        #         # make it Prop
        #         try:
        #             p = prop_config.get_conf(n, val)
        #         except:
        #             raise TypeError("Bad implementation of class '%s' in class '%s'. "\
        #                 "See example in easyvar.defaults.%s" % (vcname, class_name, vcname,))
        #         assert p is None or isinstance(p, Prop), "return value from 'get_conf' in class %s "\
        #             "inside class '%s' needs to either return None or a Prop object. See example in "\
        #             "easyvar.defaults.'%s'" % (vcname, class_name, vcname,)

        #     if isinstance(p, Prop):
        #         setattr(cls, n, p)
                # var_name = ''.join([p.var_name_prefix, n, p.var_name_suffix])

                # nofset = make_nofset(n)

                # if p.deletable:
                #     # name nfdel comes from fdel only on name (n)
                #     nfdel = make_fdel(n)
                #     main_property_fdel = cls.Props._make_fdel_plus_in_Props(n, var_name)
                # else:
                #     nfdel = make_nofdel(n)
                #     main_property_fdel = nfdel

                # if p.value is not Void:
                #     val = p.value
                # del p.value

                # dfget = make_fget_const(n, val) # used more than once
                # setattr(cls.Props._Conf, n, property(fget=make_fget_const(n, p), fset=nofset, fdel=nfdel))
                # setattr(cls.Props._Keys, n, property(fget=make_fget_const(n, n), fset=nofset, fdel=nfdel))
                # setattr(cls.Props._Defaults, n, property(fget=dfget, fset=nofset, fdel=nfdel))
                # # default value is always readonly
                # # it does not make sense to change default value later as it will
                # # have no effect because value will act on its own deepcopy version.

                # # main property configuration
                # if p.readonly:
                #     # constant value, no internal vars
                #     fset = nofset
                #     fget = dfget
                #     fdel = nfdel
                # elif p.readonly_weak:
                #     # value can not be set through property but internal var
                #     # thus value is not constant.
                #     fset = nofset
                #     fget = make_fget(n, var_name, deepcopy(val))
                #     fdel = main_property_fdel
                #     # save the internal var name in Ivan
                #     setattr(cls.Props._Ivan, n, property(fget=make_fget_const(n, var_name), fset=nofset, fdel=nfdel))
                # else:
                #     fset = make_fset(n, var_name)
                #     fget = make_fget(n, var_name, deepcopy(val))
                #     fdel = main_property_fdel
                #     # save the internal var name in Ivan
                #     setattr(cls.Props._Ivan, n, property(fget=make_fget_const(n, var_name), fset=nofset, fdel=nfdel))

                # # delattr(cls, n) # may not be needed
                # setattr(cls, n, property(fget=fget, fset=fset, fdel=fdel))

        return cls

class PropMixin(metaclass=PropMeta):
    """A base class that modifies the subclasses to define properties automatically.
    
    Each defined property will also have their configurations/metadata and default values saved in
    a special property named `Props` in the subclass.

    An example:

    ```python
    class MyClass(PropMixin):
        class VarConf():
            def get_conf(self, name, value):
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
        class VarConf():
            def get_conf(self, name, value):
                if name.lower().startswith('ro_'):
                    # variables ending with ro_ (case insensitive) will become readonly property
                    return Prop(readonly=True)
                elif name.lower().startswith('wro_'):
                    # vars ending with wro_ (case insensitive) will become properties whose
                    # values can be changed through internal variables (weak readonly).
                    return Prop(readonly_weak=True)
                elif name.lower().startswith('ndel_'):
                    # These properties won't be deletable
                    return Prop(deletable=False)
                elif: name.lower().startswith('p_'):
                    # make these normal properties whose values can be changed
                    return Prop()
                else:
                    # other attributes that do not match the above criteria
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
    VarConf = defaults.VarConf
