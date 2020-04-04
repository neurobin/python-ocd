"""Our custom types are defined here"""

class VoidType():
    """A custom type that represents false.
    
    For instances of this class, `len()` returns `0`, items and attributes can not be set.

    It's mainly used inside the containg package for null/non-existent value. `None` is a
    python object that is commonly used and should be retained its meaning as a valid value
    to a variable while we use `Void` internally to represent variables without any valid value.

    Thus, an object with `Void` value should be treated as non-existent object.
    """
    def __bool__(self):
        return False
    
    def __len__(self):
        return 0

    def __setitem__(self, key, value):
        raise NotImplementedError(self.__class__.__name__ + " does not support setting attributes")

    def __setattr__(self, key, value):
        raise NotImplementedError(self.__class__.__name__ + " does not support setting attributes")

