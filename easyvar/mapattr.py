


class BaseMap():
    """Base class for Map."""
    pass

class Attr(BaseMap):
    """A class that saves attributes and lets you iter through them
    """

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    __hash__ = BaseMap.__hash__


class MapAttr(Attr):
    """A map interface that stores items as attributes.
    
    It provides iter through keys. Values can be accessed as items or attributes.
    """

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        super(MapAttr, self).__setattr__(key, value)

    def __delitem__(self, key):
        super(MapAttr, self).__delattr__(key)


class UndeadAttrMeta(type):
    """Metaclass that makes class attributes undead"""
    
    def __delattr__(self, name):
        raise AttributeError("type(%r) does not support attribute deletion." % (self))


class ReadonlyAttrMeta(UndeadAttrMeta):
    """Metaclass that makes class attributes readonly (and undead)"""

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("type(%r) allows setting one attribute just once." % (self))
        else:
            super(ReadonlyAttrMeta, self).__setattr__(name, value)



class ReadonlyMapAttr(MapAttr, metaclass=ReadonlyAttrMeta):
    """An attribute mapping class that lets you set one item/attribute just once.

    Once set, it can not be reset or deleted.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute/item just once." % (self.__class__))
        else:
            super(ReadonlyMapAttr, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class UndeadMapAttr(MapAttr, metaclass=UndeadAttrMeta):
    """An attribute saving class that lets you make undead zombie attributes that can not be killed.
    """
    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class ReadonlyAttr(Attr, metaclass=ReadonlyAttrMeta):
    """An attribute saving class that lets you set one attribute just once.

    Once set, it can not be reset or deleted.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(ReadonlyAttr, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))



class UndeadAttr(Attr, metaclass=UndeadAttrMeta):
    """An attribute saving class that lets you make undead zombie attributes.
    """

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class ConstClass(Attr, metaclass=ReadonlyAttrMeta):
    """An attribute saving class that lets you set one attribute just the first time through class object.

    Instance object can not set any attributes.
    
    After setting the attribute, it becomes constant; neither can you reset it nor can you delete it.
    """
    
    def __setattr__(self, name, value):
        raise AttributeError("%r does not allow setting attributes through instance objects." % (self.__class__))

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))
