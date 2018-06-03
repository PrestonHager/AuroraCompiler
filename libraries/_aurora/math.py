# Aurora Math library

import math
from libraries._aurora.vars import _aurora_var_number

class AuroraMath:
    def _aurora_abs(self, num):
        num = num.get()
        if type(num) == type(0):
            return _aurora_var_number(int(math.fabs(num)))
        else:
            return _aurora_var_number(math.fabs(num))

    def _aurora_pow(self, num, pow):
        return _aurora_var_number(num.get() ** pow.get())

    def _aurora_add(self, num, num2):
        return _aurora_var_number(num.get() + num2.get())

    def _aurora_mul(self, num, num2):
        return _aurora_var_number(num.get() * num2.get())

    def _aurora_sub(self, num, num2):
        return _aurora_var_number(num.get() - num2.get())

    def _aurora_div(self, num, num2):
        num = num.get()
        num2 = num2.get()
        number = num / float(num2)
        if number % number == 0:
            return _aurora_var_number(int(number))
        return _aurora_var_number(number)

_inst = AuroraMath()
_aurora_abs = _inst._aurora_abs
_aurora_pow = _inst._aurora_pow
_aurora_add = _inst._aurora_add
_aurora_mul = _inst._aurora_mul
_aurora_sub = _inst._aurora_sub
_aurora_div = _inst._aurora_div

__all__ = ["_aurora_abs", "_aurora_pow", "_aurora_add", "_aurora_mul", "_aurora_sub", "_aurora_div"]
