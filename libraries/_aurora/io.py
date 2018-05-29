# Aurora I/O library

from sys import stdout

class AuroraIO:
    def __init__(self):
        self.stdout = open("_aurora_out", 'wb')
        self.stdin = open("_aurora_in", 'wb')

    def _aurora_print(self, *args):
        for arg in args:
            stdout.write(arg)
            self.stdout.write(arg.encode('utf-8'))
        stdout.flush()

    def _aurora_println(self, *args):
        self._aurora_print(*args+("\n",))

    def _aurora_input(self, *args):
        self._aurora_println(*args)
        read = stdin.readline()
        self.stdin.write(read.encode('utf-8'))
        return read

    def __exit__(self):
        self.stdout.close()

_inst = AuroraIO()
_aurora_print = _inst._aurora_print
_aurora_println = _inst._aurora_println
_aurora_input = _inst._aurora_input

__all__ = ["_aurora_print", "_aurora_println", "_aurora_input"]
