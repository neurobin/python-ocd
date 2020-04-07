


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


class SingleShotAttrMeta(type):
    """Make class attributes single shot"""

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("type(%r) allows setting one attribute just once." % (self))
        else:
            super(SingleShotAttrMeta, self).__setattr__(name, value)


class ReadonlyAttrMeta(SingleShotAttrMeta):
    """Make class attributes readonly"""
    
    def __delattr__(self, name):
        raise AttributeError("type(%r) does not support attribute deletion." % (self))



class SingleShotMapAttr(MapAttr, metaclass=SingleShotAttrMeta):
    """An attribute mapping class that lets you set one item/attribute just once.

    To set one attribute again, you first have to delete it.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute/item just once." % (self.__class__))
        else:
            super(SingleShotMapAttr, self).__setattr__(name, value)


class ReadonlyMapAttr(MapAttr, metaclass=ReadonlyAttrMeta):
    """An attribute saving class that lets you set one attribute just the first time.
    
    The attribute becomes constant; neither can you reset it nor can you delete it.
    """
    # TODO:
    # only immediate subclass should get the expected behavior,
    # bases is a list, for this class it's empty, len(bases) should be 1 for the first subclass
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute/item just once." % (self.__class__))
        else:
            super(ReadonlyMapAttr, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))



class SingleShotAttr(Attr, metaclass=SingleShotAttrMeta):
    """An attribute saving class that lets you set one attribute just once.

    To set one attribute again, you first have to delete it.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(SingleShotAttr, self).__setattr__(name, value)


class ReadonlyAttr(Attr, metaclass=ReadonlyAttrMeta):
    """An attribute saving class that lets you set one attribute just the first time.
    
    The attribute becomes constant; neither can you reset it nor can you delete it.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(ReadonlyAttr, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class ReadonlyClassAttr(Attr, metaclass=ReadonlyAttrMeta):
    """An attribute saving class that lets you set one attribute just the first time through class object.

    Instance object can not set any attributes.
    
    After setting the attribute, it becomes constant; neither can you reset it nor can you delete it.
    """
    
    def __setattr__(self, name, value):
        raise AttributeError("%r allows setting one attribute just once." % (self.__class__))

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))
