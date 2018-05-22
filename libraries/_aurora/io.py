# aurora I/O library

from sys import stdout

class AuroraIO:
    def _aurora_print(self, *args):
        stdout.write(args)
        stdout.flush()

    def _aurora_println(self, *args):
        stdout.write(args)
        stdout.write("\n")
        stdout.flush()

_inst = AuroraIO()
_aurora_print = _inst._aurora_print
_aurora_println = _inst._aurora_println