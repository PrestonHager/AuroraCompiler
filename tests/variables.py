from _aurora.vars import *
#  Testing Variable Definition
from _aurora.io import *
_aurora_println("Variable"," Tests")
#  Define a variable.
greeting = _aurora_var_string("Hello!")
#  and print it out.
_aurora_println(greeting.get())
#  Now for the numbers.
age = _aurora_var_number(15)
#  and see if it prints.
_aurora_println(age.string())
