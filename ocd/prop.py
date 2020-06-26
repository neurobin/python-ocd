"""Automatic property creation.

* Provides some functions to make getter and setter functions for
  various purposes.
* Provides Metaclass for Mixin classes that can be used to
  automatically create properties (with default values if given).
"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.4'


from abc import ABCMeta
from copy import deepcopy

from ocd import Void
from ocd.unro import ClassReadonly, Unro
from ocd import abc


def make_fget(name, var_name, default=Void):
    """Return a function compatible with `property()` function `fget`
    parameter

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
            raise AttributeError("Property '%s' is not set yet for %r"
                                 % (name, self,))
        return v
    return fget

def make_fget_const(name, v):
    """Make a getter for `property()` function `fget` param that
    returns a constant value.

    Args:
        name (str): name of the property
        v (any): the constant value of the property

    Raises:
        AttributeError: when the constant value is Void

    Returns:
        function: A getter function
    """
    def fget(self):
        if v is Void:
            raise AttributeError("The value of property '%s' is non-existent "
                                 "for %r. It can neither be read nor be "
                                 "written." % (name, self,))
        return v
    return fget

def make_fset(name, var_name):
    """Make a setter for `property()`'s `fset` param for property name
    and internal variable name

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
    """Make a setter for `property()`'s `fset` param that raises
    `AttributeError`

    Args:
        name (str): property name

    Raises:
        AttributeError: always raises exception

    Returns:
        function: A setter function
    """
    def fset(self, value):
        raise AttributeError("'%s' is a readonly property for %r"
                             % (name, self,))
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
            raise AttributeError("Constant readonly property '%s' can not be "
                                 "deleted by %r" % (name, self,))
    return fdel

def make_nofdel(name):
    """Make a deleter for `property()`'s `fdel` param that raises
    `AttributeError`

    Args:
        name (str): property name

    Raises:
        AttributeError: always raises exception

    Returns:
        function: A deleter function
    """
    def fdel(self):
        raise AttributeError("Property '%s' is not deletable by %r"
                             % (name, self,))
    return fdel


class Prop(Unro):
    """A class that stores configuration for a specific property"""
    # readonly options
    RO_FALSE        = 0x0000000
    RO_WEAK         = 0x0000001
    RO_STRONG       = 0x0000002
    RO_CLASS        = 0x0000004

    # undead options
    UD_FALSE        = 0x0000000
    UD_CLASS        = 0x0000001
    UD_INSTANCE     = 0x0000002

    def __init__(self, value=Void,
                 readonly=False,    # True = RO_STRONG | RO_CLASS
                 store_default=True,
                 var_name_prefix='_',
                 var_name_suffix='',
                 undead=False):     # True = UD_CLASS | UD_INSTANCE
        """Prop constructor that creates property config.

        Args:
            value (any, optional): Default value for the property.
            readonly (bool, optional): Unchangeable property. Mutable
                values can still be changed inplace. Defaults to False.
                Readonly modes can be the following:
                    RO_WEAK: Property will be readonly but changeable
                        through internal variable. Defaults to False.
                    RO_STRONG: Can not be changed through internal
                        variable because there will be no internal
                        variable.
                    RO_CLASS: Readonly at class level i.e the property
                        itself will be readonly for the defining class.
                    True: Equvalent to RO_STRONG | RO_CLASS
                    False: Not readonly
            store_default (bool, optional): Whether to store the
                default value of the property in `Props.Defaults`.
            var_name_prefix (str, optional): Prefix to add to create
                internal variable. Defaults to '_'.
            var_name_suffix (str, optional): Suffix to add to create
                internal variable. Defaults to ''.
            undead (bool, optional): Whether the property should be
                undead (non deletable). Defaults to False. Undead modes
                are following:
                    UD_CLASS: undead at class level i.e the class
                        itself won't be able to delete it.
                UD_INSTANCE: undead for instance object of the class.
                True: Equvalent to UD_CLASS | UD_INSTANCE
                False: not undead i.e deletable.

        Raises:
            ValueError: When an argument fails validation check.
        """

        def check_opt(total, opt):
            return (total & opt) != 0

        self.value = value      # Temporary attribute
        if readonly is True:
            self.readonly = Prop.RO_STRONG | Prop.RO_CLASS
        elif readonly is False:
            self.readonly = Prop.RO_FALSE
        elif isinstance(readonly, int):
            self.readonly = readonly
        else:
            raise ValueError("Invalid value for parameter 'readonly'. "
                             "Check class `Prop` for assistance.")
        if undead is True:
            self.undead = Prop.UD_CLASS | Prop.UD_INSTANCE
        elif undead is False:
            self.undead = Prop.UD_FALSE
        elif isinstance(undead, int):
            self.undead = undead
        else:
            raise ValueError("Invalid value for parameter 'undead'. "
                             "Check class `Prop` for assistance.")
        self.var_name_prefix = var_name_prefix
        self.var_name_suffix = var_name_suffix
        self.store_default = store_default

        if not isinstance(self.var_name_prefix, str) \
                or not self.var_name_prefix:
            raise ValueError("var_name_prefix needs to be a non empty string")
        elif self.var_name_prefix.startswith('__'):
            raise ValueError("Leading double underscore is not allowed in "
                             "var_name_prefix")
        elif not self.var_name_prefix.startswith('_'):
            raise ValueError("var_name_prefix must start with a single "
                             "underscore")

        if not isinstance(self.var_name_suffix, str):
            raise ValueError("var_name_suffix needs to be a string")
        elif self.var_name_suffix.endswith('__'):
            raise ValueError("Trailing double underscore is not allowed in "
                             "var_name_suffix")

        self.is_readonly = check_opt(self.readonly, Prop.RO_STRONG)
        self.is_readonly_weak = check_opt(self.readonly, Prop.RO_WEAK)
        self.is_readonly_for_class = check_opt(self.readonly, Prop.RO_CLASS)
        self.is_undead_for_instance = check_opt(self.undead, Prop.UD_INSTANCE)
        self.is_undead_for_class = check_opt(self.undead, Prop.UD_CLASS)

        if self.is_readonly_weak and self.is_readonly:
            raise ValueError("RO_WEAK and RO_STRONG can not be True at the "
                             "same time. It's either weak or strong not both")


class _Props():
    """Store information of class properties"""

    def __init__(self):
        class Keys(ClassReadonly): pass
        class Defaults(ClassReadonly): pass
        class Conf(ClassReadonly): pass
        class Ivan(ClassReadonly): pass
        self._Keys_Internal_Var = Keys()
        self._Defaults_Internal_Var = Defaults()
        self._Conf_Internal_Var = Conf()
        self._Ivan_Internal_Var = Ivan()
        self._Keys = Keys
        self._Defaults = Defaults
        self._Conf = Conf
        self._Ivan = Ivan

    def __setattr__(self, name, value):
        # print("\nsetattr %r, %s" % (self, name,))
        # if we keep these names in a single place (somewhere in some
        # variable), it would be possible to change it.
        ks = ['_Keys', '_Defaults', '_Conf', '_Ivan', '_Keys_Internal_Var',
              '_Defaults_Internal_Var', '_Conf_Internal_Var',
              '_Ivan_Internal_Var']
        if name in ks:
            # make singleton
            if name in self.__dict__:
                raise AttributeError("Attribute '%s' is reserved by %r. "
                                     "It can not be set."
                                     % (name, self.__class__,))
            else:
                super(_Props, self).__setattr__(name, value)
        else:
            super(_Props, self).__setattr__(name, value)

    def __delattr__(self, name):
        # if we keep these names in a single place (somewhere in some
        # variable), it would be possible to change it.
        ks = ['_Keys', '_Defaults', '_Conf', '_Ivan', '_Keys_Internal_Var',
              '_Defaults_Internal_Var', '_Conf_Internal_Var',
              '_Ivan_Internal_Var']
        if name in ks:
            raise AttributeError("Attribute '%s' is reserved by %r. It can "
                                 "not be deleted." % (name, self.__class__,))
        else:
            super(_Props, self).__delattr__(name)

    # property
    Keys = property(fget=make_fget('Keys', '_Keys_Internal_Var'),
                    fset=make_nofset('Keys'),
                    fdel=make_nofdel('Keys'),
                    doc='Stores the names of properties accessible by '
                        'attribute with same name. See details in doc for '
                        '`Props`.')
    Defaults = property(fget=make_fget('Defaults', '_Defaults_Internal_Var'),
                        fset=make_nofset('Defaults'),
                        fdel=make_nofdel('Defaults'),
                        doc='Stores the default values of the properties '
                            'accessible by attribute with same name. See '
                            'details in doc for `Props`.')
    Conf = property(fget=make_fget('Conf', '_Conf_Internal_Var'),
                    fset=make_nofset('Conf'),
                    fdel=make_nofdel('Conf'),
                    doc='Stores configuration of the properties accessible '
                        'by attribute with same name. See details in doc for '
                        '`Props`.')

    Ivan = property(fget=make_fget('Ivan', '_Ivan_Internal_Var'),
                    fset=make_nofset('Ivan'),
                    fdel=make_nofdel('Ivan'),
                    doc='Stores the internal variable names of the properties'
                        ' accessible by attribute with same name. See details'
                        ' in doc for `Props`.')

    # Convenience aliases
    K = Keys
    D = Defaults
    C = Conf
    I = Ivan


class PropMeta(ABCMeta):
    """Metaclass for `PropMixin` that will modify the subclasses to
    define properties automatically.

    Do note that this is a metaclass, you don't need to inherit it,
    rather inherit the `PropMixin` class.
    The `Props` attribute of this class will be available through your
    class name. For example:

    ```python
    class MyClass(PropMixin):
        my_property = Prop('Building A/2')

    default_value = MyClass.Props.Defaults.my_property
    ```
    """

    Props = property(fget=make_fget('Props', '_Props_'),
                     fset=make_nofset('Props'),
                     fdel=make_nofdel('Props'),
                     doc="""This attribute contains some other attributes to
                     provide more information about properties.

                     Keys
                     ====
                     Contains the name of the properties accessible as
                     attributes. For example, an attribute named 'author_name'
                     can be accessed as: `Props.Keys.author_name`. It will
                     return the name of the attribute as string: 'author_name'

                     Defaults
                     ========
                     Stores the default values of properties.

                     `Props.Defaults.author_name` will return the default
                     value of `author_name` attribute.

                     Conf
                     ====
                     Stores the configuration of property.

                     `Props.Conf.author_name` will return a `Prop` object.

                     Ivan
                     ====
                     Stores the internal variable name of property.

                     `Props.Ivan.author_name` will return the name of the
                     internal variable for `author_name` property as `str`.
                     """)

    def __delattr__(self, name):
        # if we keep this name in a single place (somewhere in some
        # variable), it would be possible to change it.
        if name == '_Props_':
            raise AttributeError("'%s' is reserved by %r as an internal "
                                 "variable name. It can not be deleted."
                                 % (name, self.__class__,))
        try:
            isProp = getattr(self.Props.Conf, name)
            # ^returns None or Prop()
            # if None, then it's not a property
        except:
            isProp = None
        if isProp:
            if isProp.is_undead_for_class:
                raise AttributeError("Property '%s' is not deletable by %r"
                                     % (name, self,))
            delattr(self.Props._Keys, name)
            delattr(self.Props._Conf, name)
            if hasattr(self.Props._Defaults, name):
                delattr(self.Props._Defaults, name)
            # unlike others internal variable is not always available:
            if hasattr(self.Props._Ivan, name):
                delattr(self.Props._Ivan, name)
        super(PropMeta, self).__delattr__(name)

    def __setattr__(self, name, value):
        # if we keep this name in a single place (somewhere in some
        # variable), it would be possible to change it.
        if name == '_Props_':
            if name in self.__dict__:
                raise AttributeError("'%s' is reserved by %r as an internal "
                                     "variable name."
                                     % (name, self.__class__,))
            else:
                super(PropMeta, self).__setattr__(name, value)
        else:
            reserved = ['VarConf',]
            if name in reserved:
                raise AttributeError("Attribute name '%s' is reserved by %r."
                                     % (name, self.__class__,))
            if not name.startswith('_'):
                try:
                    prop = getattr(self.Props.Conf, name, None)
                except:
                    prop = None
                if isinstance(prop, Prop):
                    # trying to overwrite a Prop() definition itself.
                    # should we allow it?
                    # ...
                    # !!?
                    # give option: check whether it should be allowed
                    # or not
                    if prop.is_readonly_for_class:
                        raise AttributeError("Property '%s' is readonly for "
                                             "%r" % (name, self,))

                if not isinstance(value, Prop):
                    val = value
                    p = self._get_var_conf(name, value)
                    if p:
                        # returned a Prop, this one needs to be
                        # converted to property
                        value = p
                else:
                    # value is Prop
                    val = value.value

                # now value is OK for final processing
                if isinstance(value, Prop):
                    # print("Creating property '%s' for class '%r'"
                    #       % (name, self))
                    (This_Prop,
                     Defaults_Prop,
                     Keys_Prop,
                     Ivan_Prop,
                     Conf_Prop) = self._makePropProperties(name, value, val)
                    super(PropMeta, self).__setattr__(name, This_Prop)
                    setattr(self.Props._Conf, name, Conf_Prop)
                    setattr(self.Props._Keys, name, Keys_Prop)
                    if Defaults_Prop:
                        setattr(self.Props._Defaults, name, Defaults_Prop)
                    # unlike others internal variable is not always
                    # available:
                    if Ivan_Prop:
                        setattr(self.Props._Ivan, name, Ivan_Prop)
                else:
                    super(PropMeta, self).__setattr__(name, value)
            else:
                super(PropMeta, self).__setattr__(name, value)


    def _makePropProperties(self, n, p, val):
        """Return a tuple of all property objects"""
        var_name = ''.join([p.var_name_prefix, n, p.var_name_suffix])

        nofset = make_nofset(n)

        if not p.is_undead_for_instance:
            # name nfdel comes from fdel only on name (n)
            nfdel = make_fdel(n)
            main_property_fdel = make_fdel(n, var_name)
        else:
            nfdel = make_nofdel(n)
            main_property_fdel = nfdel

        dfget = make_fget_const(n, val) # used more than once
        Conf_Prop = property(fget=make_fget_const(n, p), fset=nofset,
                             fdel=nfdel)
        Keys_Prop = property(fget=make_fget_const(n, n), fset=nofset,
                             fdel=nfdel)
        if p.store_default:
            Defaults_Prop = property(fget=dfget, fset=nofset, fdel=nfdel)
        else:
            Defaults_Prop = None
        Ivan_Prop = None
        # default value is always readonly ^:
        # it does not make sense to change default value later as it
        # will have no effect because value will act on its own
        # deepcopy version.

        # main property configuration
        if p.is_readonly:
            # constant value, no internal vars
            fset = nofset
            fget = dfget
            fdel = nfdel
        elif p.is_readonly_weak:
            # value can not be set through property but internal var
            # thus value is not constant.
            fset = nofset
            fget = make_fget(n, var_name, deepcopy(val))
            fdel = main_property_fdel
            # save the internal var name in Ivan
            Ivan_Prop = property(fget=make_fget_const(n, var_name),
                                 fset=nofset, fdel=nfdel)
        else:
            fset = make_fset(n, var_name)
            fget = make_fget(n, var_name, deepcopy(val))
            fdel = main_property_fdel
            # save the internal var name in Ivan
            Ivan_Prop = property(fget=make_fget_const(n, var_name),
                                 fset=nofset, fdel=nfdel)

        This_Prop = property(fget=fget, fset=fset, fdel=fdel)
        return This_Prop, Defaults_Prop, Keys_Prop, Ivan_Prop, Conf_Prop

    def _get_var_conf(self, name, value):
        """Either return Prop object or None"""
        # print("\nchecking var_conf for "+name)
        try:
            var_conf = self.VarConf()
        except:
            raise TypeError("'VarConf' is a reserved attribute name. It must "
                            "be a class that inherits and implements "
                            "`ocd.abc.VarConf`.")
        if isinstance(var_conf, abc.VarConf): # must do this check
            # because if some other class implementation provide
            # get_conf method with name/value arg,
            # we do not want to accept unknown entities.
            try:
                p = var_conf.get_conf(name, value)
            except:
                raise TypeError("Bad implementation of `VarConf` class. See "
                                "`ocd.abc.VarConf`")
        else:
            raise TypeError("'VarConf' is a reserved attribute name. It must "
                            "be a class that inherits and implements "
                            "`ocd.abc.VarConf`.")
        assert p is None or isinstance(p, Prop), "return value from "\
                                                 "'get_conf' in class "\
                                                 "'VarConf' inside class "\
                                                 "'%r' needs to either "\
                                                 "return `None` or a `Prop`"\
                                                 " object. See example in "\
                                                 "`ocd.abc.VarConf`"\
                                                 % (self.__class__,)
        return p

    # def __init__(cls, name, bases, attrs):
    #     super(PropMeta, cls).__init__(name, bases, attrs)

    def __new__(mcs, class_name, bases, attrs):
        rserved_attrs = ['Props', '_Props_']
        for K in rserved_attrs:
            if K in attrs:
                raise AttributeError("'%s' is a reserved attribute for class"
                                     "'%s' defined in '%r'. Please do not "
                                     "redefine it." % (K, class_name, mcs,))
        cls = super(PropMeta, mcs).__new__(mcs, class_name, bases, attrs)
        cls._Props_ = _Props()
        # prop_candidates = {}
        non_candidates = ['VarConf']
        for k in attrs:
            if k.startswith('_') or k in non_candidates:
                pass
            else:
                # print("\n" + k)
                setattr(cls, k, attrs[k])

        return cls
