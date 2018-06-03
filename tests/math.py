from _aurora.vars import *
#  Testing the Aurora Math Library
from _aurora.math import *
from _aurora.io import *
_aurora_println(_aurora_var_string("Testing builtin math"))
#  Test to see if 1 + 1 = 2
two = _aurora_var_number(1+1)
_aurora_print(_aurora_var_string("1 + 1 = "))
_aurora_println(two.string())
#  Test to see if 15 - 9 = 6
six = _aurora_var_number(15-9)
_aurora_print(_aurora_var_string("15 - 9 = "))
_aurora_println(six.string())
#  Test to see if 5 * 12 = 60
sixty = _aurora_var_number(5*12)
_aurora_print(_aurora_var_string("5 * 12 = "))
_aurora_println(sixty.string())
#  Test to see if 100 / 25 = 4
quarter = _aurora_var_number(100/25)
_aurora_print(_aurora_var_string("100 / 25 = "))
_aurora_println(quarter.string())
_aurora_println(_aurora_var_string("Testing Math Library"))
#  Check to see if 7+2 + 8 = 17
age = _aurora_add(_aurora_var_number(7+2),_aurora_var_number(8))
_aurora_print(_aurora_var_string("7+2 + 8 = "))
_aurora_println(age.string())
#  Check to see if 4 * 3 = 12
twelve = _aurora_mul(_aurora_var_number(3),_aurora_var_number(4))
_aurora_print(_aurora_var_string("4 * 3 = "))
_aurora_println(twelve.string())
#  Check to see if 2 ^ 4 = 16
power_two = _aurora_pow(_aurora_var_number(2),_aurora_var_number(4))
_aurora_print(_aurora_var_string("2 ^ 4 = "))
_aurora_println(power_two.string())
#  Check to see if 0 - 24 = -24
negitive_twenty_four = _aurora_sub(_aurora_var_number(0),_aurora_var_number(24))
_aurora_print(_aurora_var_string("0 - 24 = "))
_aurora_println(negitive_twenty_four.string())
#  Check to see if 1 / 2 = 0.5
half = _aurora_div(_aurora_var_number(1),_aurora_var_number(2))
_aurora_print(_aurora_var_string("1 / 2 = "))
_aurora_println(half.string())
#  Check to see if |-52| = 52 = |52|
negitive_abs = _aurora_abs(_aurora_var_number(-52))
positive_abs = _aurora_abs(_aurora_var_number(52))
_aurora_print(_aurora_var_string("|-52| = "))
_aurora_println(negitive_abs.string())
_aurora_print(_aurora_var_string("|52| = "))
_aurora_println(positive_abs.string())
