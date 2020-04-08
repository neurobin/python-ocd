"""Our custom types are defined here"""


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class VoidType(object, metaclass=SingletonMeta):
    """A custom type that represents false.
    
    For instances of this class, `len()` returns `0`, items and attributes can not be set.

    It's mainly used inside the containing package for null/non-existent value. `None` is a
    python object that is commonly used and should be retained its meaning as a valid value
    to a variable while we use `Void` internally to represent variables without any valid value.

    Thus, an object with `Void` value should be treated as non-existent object.
    """

    def __new__(cls):
        return Void
    def __reduce__(self):
        return (VoidType, ())
    def __copy__(self):
        return Void
    def __deepcopy__(self, memo):
        return Void
    def __call__(self, default):
        pass

    def __bool__(self):
        return False
    
    def __len__(self):
        return 0

    def __setitem__(self, key, value):
        raise NotImplementedError(self.__class__.__name__ + " does not support setting attributes")

    def __setattr__(self, key, value):
        raise NotImplementedError(self.__class__.__name__ + " does not support setting attributes")

Void = object.__new__(VoidType)