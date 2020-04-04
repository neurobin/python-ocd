
from pprint import pformat

class BaseMap():
    """Base class for Map."""
    pass

class MapAttr(BaseMap):
    """A map interface that stores items as attributes
    
    It only provides iter through keys.
    Values can be accessed as items or attributes.
    """

    def __init__(self, *args, **kwargs):
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    __hash__ = BaseMap.__hash__

    def __repr__(self):
        return pformat(self.__dict__)
    
    def __call__(self, keys_only=False):
        if keys_only:
            return self.__dict__.keys()
        return self.__dict__

m = MapAttr()
m._value = 34
m.data = 'test'

print('data' in m)
print(m.__dict__)
print(m['data'])
