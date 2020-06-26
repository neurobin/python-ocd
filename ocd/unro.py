"""Undead and readonly attribute classes.

Undead class attributes are non deletable and Readonly class attributes
are readonly. Unro class attributes are both non deletable and readonly

Two types of classes are to be found here:

1. Attribute saving class that does not let you access the attributes as items
2. Attribute mapping class that lets you access the attributes as items.
"""

__author__ = 'Md Jahidul Hamid <jahidulhamid@yahoo.com>'
__copyright__ = 'Copyright © Md Jahidul Hamid <https://github.com/neurobin/>'
__license__ = '[BSD](http://www.opensource.org/licenses/bsd-license.php)'
__version__ = '0.0.4'


class _Object(object):
    """Base class for all."""
    pass

class _Base(_Object):
    """A class that saves attributes and lets you iter through them
    """

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    __hash__ = _Object.__hash__


class _Map(_Base):
    """A map interface that stores items as attributes.

    It provides iter through keys. Values can be accessed as items or
    attributes.
    """

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)


#######################################################################
##################### Some meta classes ###############################
#######################################################################

class _UndeadMeta(type):
    """Metaclass that makes class attributes undead (not deletable)"""

    def __delattr__(self, name):
        raise AttributeError("type(%r) does not support attribute deletion."
                            % (self))


class _UndeadMapMeta(_UndeadMeta):
    """Metaclass that makes class attributes undead (not deletable).

    Attributes are accessible as items.
    """

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        super(_UndeadMapMeta, self).__setattr__(key, value)

    def __delitem__(self, key):
        super(_UndeadMapMeta, self).__delattr__(key)


class _ReadonlyMeta(type):
    """Metaclass that makes class attributes readonly"""

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("type(%r) allows setting one attribute just "
                                 "once." % (self))
        else:
            super(_ReadonlyMeta, self).__setattr__(name, value)


class _ReadonlyMapMeta(_ReadonlyMeta):
    """Metaclass that makes class attributes readonly where attributes
    are accessible as items.
    """

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        super(_ReadonlyMapMeta, self).__setattr__(key, value)

    def __delitem__(self, key):
        super(_ReadonlyMapMeta, self).__delattr__(key)


class _UnroMeta(_UndeadMeta, _ReadonlyMeta):
    """Metaclass that makes attributes undead (not deletable) and
    readonly
    """
    pass


class _UnroMapMeta(_UnroMeta):
    """Metaclass that makes attributes undead (not deletable) and
    readonly where attributes are accessible as items.
    """

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        super(_UnroMapMeta, self).__setattr__(key, value)

    def __delitem__(self, key):
        super(_UnroMapMeta, self).__delattr__(key)

#######################################################################


#######################################################################
################# Some class readonly attr storage class ##############
#######################################################################


class ClassReadonlyMap(_Map, metaclass=_ReadonlyMapMeta):
    """An attribute mapping class that lets you set one class attribute
    just once.

    Once set, it can not be reset (unless deleted).

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassReadonly(_Base, metaclass=_ReadonlyMeta):
    """An attribute saving class that lets you set one class attribute
    just once.

    Once set, it can not be reset (unless deleted).

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUndeadMap(_Map, metaclass=_UndeadMapMeta):
    """An attribute mapping class that lets you make undead class
    attributes that can not be killed.

    Once set, it can not be deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUndead(_Base, metaclass=_UndeadMeta):
    """An attribute saving class that lets you make undead class
    attributes that can not be killed.

    Once set, it can not be deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUnro(_Base, metaclass=_UnroMeta):
    """An attribute saving class that lets you make unro
    (undead + readonly) class attributes that can not be killed.

    Once set, it can not be reset or deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassUnroMap(_Map, metaclass=_UnroMapMeta):
    """An attribute mapping class that lets you make unro
    (undead and readonly) class attributes that can not be killed.

    Once set, it can not be reset or deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


#######################################################################


#######################################################################
### Some attribute storage class that impose same restrictions ########
### upon both class attributes and instance attributes ################
#######################################################################

class ReadonlyMap(_Map, metaclass=_ReadonlyMapMeta):
    """An attribute mapping class that lets you set one item/attribute
    just once.

    Once set, it can not be reset (unless deleted).

    Restriction imposed upon both class attributes and and instance
    attributes equally.
    """

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute/item "
                                 "just once." % (self.__class__))
        else:
            super(ReadonlyMap, self).__setattr__(name, value)


class Readonly(_Base, metaclass=_ReadonlyMeta):
    """An attribute saving class that lets you set one attribute just
    once.

    Once set, it can not be reset (unless deleted).

    Restriction imposed upon both class attributes and and instance
    attributes equally.
    """

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once."
                                 % (self.__class__))
        else:
            super(Readonly, self).__setattr__(name, value)


class UndeadMap(_Map, metaclass=_UndeadMapMeta):
    """An attribute mapping class that lets you make undead attributes
    that can not be killed.

    Restriction imposed upon both class attributes and and instance
    attributes equally.
    """
    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion."
                             % (self.__class__))


class Undead(_Base, metaclass=_UndeadMeta):
    """An attribute saving class that lets you make undead attributes
    that can not be killed.

    Restriction imposed upon both class attributes and and instance
    attributes equally.
    """
    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion."
                             % (self.__class__))


class Unro(_Base, metaclass=_UnroMeta):
    """An attribute saving class that lets you set one attribute just
    once.

    Once set, it can not be reset or deleted.

    Restriction imposed upon both class attributes and and instance
    attributes equally.
    """

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once."
                                 % (self.__class__))
        else:
            super(Unro, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion."
                             % (self.__class__))


class UnroMap(_Map, metaclass=_UnroMapMeta):
    """An attribute mapping class that lets you set one attribute
    just once.

    Once set, it can not be reset or deleted.

    Restriction imposed upon both class attributes and and instance
    attributes equally.
    """

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once."
                                 % (self.__class__))
        else:
            super(UnroMap, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion."
                             % (self.__class__))


#######################################################################
######## Some more specialized class ##################################
#######################################################################


class ConstClass(ClassUnro):
    """An attribute saving class that lets you set one attribute just
    the first time through class object.

    Instance object can not set any attributes.

    After setting the attribute, it becomes constant; neither can you
    reset it nor can you delete it.
    """

    def __setattr__(self, name, value):
        raise AttributeError("%r does not allow setting attributes through "
                             "instance objects." % (self.__class__))

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion."
                             % (self.__class__))


class ConstClassMap(ClassUnroMap):
    """An attribute mapping class that lets you set one attribute/item
    just the first time through class object.

    Instance object can not set any attributes.

    After setting the attribute, it becomes constant; neither can you
    reset it nor can you delete it.
    """

    def __setattr__(self, name, value):
        raise AttributeError("%r does not allow setting attributes through "
                             "instance objects." % (self.__class__))

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion."
                             % (self.__class__))


#######################################################################
