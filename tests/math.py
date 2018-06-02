from _aurora.vars import *
#  Testing the Aurora Math Library
from _aurora.math import *
from _aurora.io import *
_aurora_println("Testing Math Library")
#  Check to see if 7 + 8 = 15
age = _aurora_var_number(_aurora_add(7,8))
_aurora_print("7 + 8 = ")
_aurora_println(age.string())
#  Check to see if 4 * 3 = 12
twelve = _aurora_var_number(_aurora_mul(3,4))
_aurora_print("4 * 3 = ")
_aurora_println(twelve.string())
