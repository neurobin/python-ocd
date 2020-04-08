


class BaseMap(object):
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


####################################################################
##################### Some meta classes ############################
####################################################################

class ZombieAttrMeta(type):
    """Metaclass that makes class attributes zombie (not deletable)"""
    
    def __delattr__(self, name):
        raise AttributeError("type(%r) does not support attribute deletion." % (self))


class ReadonlyAttrMeta(type):
    """Metaclass that makes class attributes readonly"""

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("type(%r) allows setting one attribute just once." % (self))
        else:
            super(ReadonlyAttrMeta, self).__setattr__(name, value)

class ZomroAttrMeta(ZombieAttrMeta, ReadonlyAttrMeta):
    """Metaclass that makes attributes zombie (not deletable) and readonly
    """
    pass

####################################################################
####################################################################


#####################################################################
################# Some class readonly attr storage class ############
#####################################################################


class ClassReadonlyMapAttr(MapAttr, metaclass=ReadonlyAttrMeta):
    """An attribute mapping class that lets you set one class attribute just once.

    Once set, it can not be reset (unless deleted).

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassReadonlyAttr(Attr, metaclass=ReadonlyAttrMeta):
    """An attribute saving class that lets you set one class attribute just once.

    Once set, it can not be reset (unless deleted).

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassZombieMapAttr(MapAttr, metaclass=ZombieAttrMeta):
    """An attribute mapping class that lets you make zombie class attributes that can not be killed.

    Once set, it can not be deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassZombieAttr(Attr, metaclass=ZombieAttrMeta):
    """An attribute saving class that lets you make zombie class attributes that can not be killed.

    Once set, it can not be deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassZomroAttr(Attr, metaclass=ZomroAttrMeta):
    """An attribute saving class that lets you make zomro (zombie and readonly)
    attributes that can not be killed.

    Once set, it can not be reset or deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


class ClassZomroMapAttr(MapAttr, metaclass=ZomroAttrMeta):
    """An attribute mapping class that lets you make zomro (zombie and readonly)
    attributes that can not be killed.

    Once set, it can not be reset or deleted.

    There is no restriction imposed upon instance attributes.
    """
    pass


#####################################################################
#####################################################################


#####################################################################
### Some attribute storage class that impose same restrictions ######
### upon both class attributes and instance attributes ##############
#####################################################################

class ReadonlyMapAttr(MapAttr, metaclass=ReadonlyAttrMeta):
    """An attribute mapping class that lets you set one item/attribute just once.

    Once set, it can not be reset (unless deleted).

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute/item just once." % (self.__class__))
        else:
            super(ReadonlyMapAttr, self).__setattr__(name, value)


class ReadonlyAttr(Attr, metaclass=ReadonlyAttrMeta):
    """An attribute saving class that lets you set one item/attribute just once.

    Once set, it can not be reset (unless deleted).

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(ReadonlyAttr, self).__setattr__(name, value)


class ZombieMapAttr(MapAttr, metaclass=ZombieAttrMeta):
    """An attribute mapping class that lets you make zombie attributes that can not be killed.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class ZombieAttr(Attr, metaclass=ZombieAttrMeta):
    """An attribute saving class that lets you make zombie attributes that can not be killed.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class ZomroAttr(Attr, metaclass=ZomroAttrMeta):
    """An attribute saving class that lets you set one attribute just once.

    Once set, it can not be reset or deleted.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(ZomroAttr, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


class ZomroMapAttr(MapAttr, metaclass=ZomroAttrMeta):
    """An attribute mapping class that lets you set one attribute just once.

    Once set, it can not be reset or deleted.

    Restriction imposed upon both class attributes and and instance attributes equally.
    """
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("%r allows setting one attribute just once." % (self.__class__))
        else:
            super(ZomroMapAttr, self).__setattr__(name, value)

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))


####################################################################################################
######## Some more specialized class ###############################################################
####################################################################################################

class ConstClass(ClassZomroAttr):
    """An attribute saving class that lets you set one attribute just the first time through class object.

    Instance object can not set any attributes.
    
    After setting the attribute, it becomes constant; neither can you reset it nor can you delete it.
    """
    
    def __setattr__(self, name, value):
        raise AttributeError("%r does not allow setting attributes through instance objects." % (self.__class__))

    def __delattr__(self, name):
        raise AttributeError("class %r does not support attribute deletion." % (self.__class__))

####################################################################################################
####################################################################################################