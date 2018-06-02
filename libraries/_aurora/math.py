# Aurora Math library

import math

class AuroraMath:
    def _aurora_abs(self, num):
        return math.abs(num)

    def _aurora_pow(self, num, pow):
        return math.pow(num, pow)

    def _aurora_add(self, num, num2):
        return num + num2

    def _aurora_mul(self, num, num2):
        return num * num2

_inst = AuroraMath()
_aurora_abs = _inst._aurora_abs
_aurora_pow = _inst._aurora_pow
_aurora_add = _inst._aurora_add
_aurora_mul = _inst._aurora_mul

__all__ = ["_aurora_abs", "_aurora_pow", "_aurora_add", "_aurora_mul"]
