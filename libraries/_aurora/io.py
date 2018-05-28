# Aurora I/O library

from sys import stdout

class AuroraIO:
    def _aurora_print(self, *args):
        for arg in args:
            stdout.write(arg)
        stdout.flush()

    def _aurora_println(self, *args):
        self._aurora_print(*args)
        stdout.write("\n")
        stdout.flush()

    def _aurora_input(self, *args):
        self._aurora_println(*args)
        return stdin.readline()

_inst = AuroraIO()
_aurora_print = _inst._aurora_print
_aurora_println = _inst._aurora_println
_aurora_input = _inst._aurora_input

__all__ = ["_aurora_print", "_aurora_println", "_aurora_input"]
