

import decimal

from ..field import Field


class Money(Field):
    """A base class for Money field
    
    Inherit and expand to support full money validation
    """
    def __init__(self, name, round_direction=decimal.ROUND_HALF_UP, **kwargs):
        self.__round_direction = round_direction
        dtype = kwargs.pop(Field.Key.dtype__key, decimal.Decimal)
        mod = kwargs.pop(Field.Key.mod, self._my_custom_mod)
        super(Money, self).__init__(name, dtype=dtype, mod=mod, **kwargs)

    def _my_custom_mod(self, value):
        """Modify value so that it passes validation checks
        
        Also make sure it has 2 digits precision
        """
        value = decimal.Decimal(value)
        return value.quantize(decimal.Decimal(".01"), rounding=self.__round_direction)

