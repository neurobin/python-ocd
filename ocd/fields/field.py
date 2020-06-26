
import logging

from .defaults import VoidType, Mod, Validator, Void


UPPER_CASE = 1
LOWER_CASE = 2
NO_CASE = 0


class Field():
    """Metadata for fields such as validators, modifiers etc..."""

    class Key():
        dtype = 'dtype'
        validator = 'validator'
        mod = 'mod'
        default = 'default'
        icase = 'icase'
        case = 'case'
        help_text = 'help_text'
        log_level = 'log_level'
        errors = 'errors'


    def __init__(self, name, **kwargs):

        if not isinstance(name, str):
            raise ValueError("name must be of type str not %r" % (type(name),))

        self.__name = name
        self.__dtype = kwargs.pop(self.Key.dtype, VoidType)
        self.__validator = kwargs.pop(self.Key.validator, Validator())
        self.__mod = kwargs.pop(self.Key.mod, Mod())
        self.__default = kwargs.pop(self.Key.default, Void)
        self.__icase = kwargs.pop(self.Key.icase, False)
        self.__case = kwargs.pop(self.Key.case, NO_CASE)
        self.__help_text = kwargs.pop(self.Key.help_text, '')
        self.__log_level = kwargs.pop(self.Key.log_level, logging.DEBUG)
        self.errors = kwargs.pop(self.Key.errors, False)                    # modifiable on the fly

        for k in kwargs:
            raise KeyError("Unrecognized keyword argument: %s" % (k,))

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(self.__log_level)
        self.log = self.logger      # Convenience alias

        if self.__icase:
            self.__iname = self.__name.lower()
        else:
            self.__iname = self.__name

        if self.__case == UPPER_CASE:
            self.__name = self.__name.upper()
        elif self.__case == LOWER_CASE:
            self.__name = self.__name.lower()

        if self.__default is Void:
            self.__default = self.clean(self.__dtype())
        else:
            self.__default = self.clean(self.__default)
    
    def clean(self, value):
        value = self.__mod(value) # Our Mod() returns unmodified value, thus a single call can do the job without using any additional conditional

        if isinstance(value, self.__dtype) or self.__dtype is VoidType: # instance check first for performance as it will appear in most cases
            if not self.__validator(value): # Our Validator() always returns True, no need to check whether validator is passed or not.
                error_msg = "Value %s failed to pass the validator: %r" % (value, self.__validator,)
                if self.errors:
                    raise ValueError(error_msg)
                else:
                    self.logger.warning(error_msg)
        else:
            raise TypeError("Passed value %s is not of type %s" % (value, self.__dtype,))
        return value

    
    def __str__(self):
        return self.__name
    
    def __repr__(self):
        return self.__class__.__name__
    
    def __hash__(self):
        return hash(self.__iname)

    def __eq__(self, other): 
        return self.__iname == other.__iname
    
    def __lt__(self, other):
        return self.__iname < other.__iname

    def __gt__(self, other):
        return self.__iname > other.__iname
    
    @property
    def help_text(self):
        return self.__help_text
    
    @property
    def default(self):
        return self.__default
    
    @property
    def name(self):
        return self.__name
    
    @property
    def iname(self):
        return self.__iname
    
    @property
    def case(self):
        return self.__case
    
    @property
    def icase(self):
        return self.__icase
    
    @property
    def dtype(self):
        return self.__dtype
    
    @property
    def validator(self):
        return self.__validator
    
    @property
    def mod(self):
        return self.__mod