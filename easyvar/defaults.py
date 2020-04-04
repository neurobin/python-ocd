
class VoidType():
    """A custom type that represents false"""
    def __bool__(self):
        return False
    
    def __len__(self):
        return 0

    def __setitem__(self, key, value):
        raise NotImplementedError(self.__class__.__name__ + " does not support setting attributes")

    def __setattr__(self, key, value):
        raise NotImplementedError(self.__class__.__name__ + " does not support setting attributes")

Void = VoidType()


class Mod(VoidType):
    """A modifier that does not modify the value"""
    def __call__(self, value):
        return value


class Validator(VoidType):
    """A validator that always says 'Valid'"""
    def __call__(self, value):
        return True


