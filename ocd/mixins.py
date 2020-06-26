"""Mixin classes.
"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.4'


from ocd import defaults
from ocd.prop import PropMeta


class PropMixin(metaclass=PropMeta):
    """A base class that modifies the subclasses to define properties
    automatically.

    Each defined property will also have their configurations/metadata
    and default values saved in a special property named `Props` in
    the subclass.

    An example:

    ```python
    class MyClass(PropMixin):
        class VarConf(defaults.VarConfNone):
            def get_conf(self, name, value):
                return Prop(readonly=True)

        author_name = 'Jahidul Hamid'
        version = 'Some version'
        etc = 'etc...'
    ```

    The above class's attributes will be converted to readonly
    properties. Thus, when you do:

    ```python
    m = MyClass()
    m.author_name = 'John Doe' # throws AttributeError
    ```

    It will throw `AttributeError` saying that you are trying to modify
    a readonly property. Thus the objects of this class can only access
    the property and not modify it.

    However, mutable values can still be changed inplace :D.

    You can not change the value of the property like `m._author_name`
    as no internal variable is created when `readonly=True`. If you
    need internal variables, pass `readonly=Prop.RO_WEAK` which will
    let you change the values through internal variables. By the way,
    all mingling with protected variables like `m._author_name` should
    be done inside instance method definitions. The name of the
    internal variable `_author_name` will be made up by prefixing the
    property name with a single underscore. You can set up custom
    prefix and suffix (check the options provided by `Prop`)

    Other than creating the property it does several other things. It
    creates a special property named `Props` in your class (`MyClass`)
    and stores some information and default values in it.

    Mixed type of properties
    ========================

    In above, all class attributes were being converted to **readonly**
    property. Now let's see how we can have mixed types of properties:

    ```python
    class MyClass(PropMixin):
        class VarConf(defaults.VarConfNone):
            def get_conf(self, name, value):
                if name.lower().startswith('ro_'):
                    # variables starting with ro_ (case insensitive)
                    # will become readonly property
                    return Prop(readonly=True)
                elif name.lower().startswith('wro_'):
                    # vars starting with wro_ (case insensitive) will
                    # become properties whose values can be changed
                    # through internal variables  (weak readonly).
                    return Prop(readonly=Prop.RO_WEAK)
                elif name.lower().startswith('ndel_'):
                    # These properties won't be deletable
                    return Prop(undead=True)
                elif: name.lower().startswith('p_'):
                    # make these normal properties whose values can be
                    # changed
                    return Prop()
                else:
                    # other attributes that do not match the above
                    # criteria won't be converted to properties.
                    return None

        # These won't be converted to properties
        author_name = 'John Doe'
        version = 'Some version'
        etc = 'etc...'

        # These will become readonly properties
        ro_author_name = 'John Doe'
        ro_version = 'Some version'
        ro_etc = 'etc...'

        # weak readonly properties that can be changed with internal
        # vars
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

    `Props` attribute provides some information about the properties.
    The following table should depict what information can be accessed
    by `Props`.

    Attribute  | Short | Details
    ---------- | ----- | -------
    `Keys`     | `K`     | `MyClass.Props.Keys.author_name` will \
                            return 'author_name' (the name of the \
                            property)
    `Defaults` | `D`     | `MyClass.Props.Defaults.author_name` will \
                            return 'John Doe' (the default value)
    `Conf`     | `M`     | `MyClass.Props.Conf.author_name` will \
                            return a `Prop` object for `author_name`
    `Ivan`     | `I`     | `MyClass.Props.Ivan.author_name` will \
                            return '_author_name' (internal variable \
                            name)

    Note
    ====

    * We do not allow variables starting with an underscores to be
      converted to property.
    * Variables with leading underscore can store `Prop` class objects
      without getting converted to property.

    """
    VarConf = defaults.VarConfNone
