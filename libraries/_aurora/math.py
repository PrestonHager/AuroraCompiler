# Aurora Math library

import math

class AuroraMath:
    def _aurora_abs(self, num):
        if type(num) == type(0):
            return int(math.fabs(num))
        else:
            return math.fabs(num)

    def _aurora_pow(self, num, pow):
        return num ** pow

    def _aurora_add(self, num, num2):
        return num + num2

    def _aurora_mul(self, num, num2):
        return num * num2

    def _aurora_sub(self, num, num2):
        return num - num2

    def _aurora_div(self, num, num2):
        number = num / float(num2)
        if number % number == 0:
            return int(number)
        return number

_inst = AuroraMath()
_aurora_abs = _inst._aurora_abs
_aurora_pow = _inst._aurora_pow
_aurora_add = _inst._aurora_add
_aurora_mul = _inst._aurora_mul
_aurora_sub = _inst._aurora_sub
_aurora_div = _inst._aurora_div

__all__ = ["_aurora_abs", "_aurora_pow", "_aurora_add", "_aurora_mul", "_aurora_sub", "_aurora_div"]
