from libraries._aurora.vars import *
#  Testing the Aurora Math Library
from libraries._aurora.io import *
#  Debug print
print(dir())
_aurora_println(_aurora_var_string("Debug...!"))
#  Define greet function
def greet(name):
  global _aurora_include,_aurora_println,greet,_aurora_print
  _aurora_print(_aurora_var_string("Hello, "))
  _aurora_println(name)

#  Greet the person, Pi
greet(_aurora_var_string("Pi"))
