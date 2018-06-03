# Aurora I/O library

from sys import stdout, stdin
from libraries._aurora.vars import _aurora_var_string

class AuroraIO:
    def _aurora_print(self, *args):
        for arg in args:
            stdout.write(arg.get())
        stdout.flush()

    def _aurora_println(self, *args):
        self._aurora_print(*args+(_aurora_var_string("\n"),))

    def _aurora_input(self, *args):
        self._aurora_println(*args)
        read = stdin.readline()
        return read

_inst = AuroraIO()
_aurora_print = _inst._aurora_print
_aurora_println = _inst._aurora_println
_aurora_input = _inst._aurora_input

__all__ = ["_aurora_print", "_aurora_println", "_aurora_input"]
