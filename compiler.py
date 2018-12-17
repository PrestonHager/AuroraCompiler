# compiler.py
# by Preston Hager
# for Aurora Compiler

from utils.lexer import *
from utils.parser import *

class Compiler:
    def __init__(self, file=None, text=None):
        if file != None:
            with open(file, 'r') as f_in:
                code = f_in.read()
        elif text != None:
            code = text
        else:
            raise Exception("No code input found. Please supply either a file or text.")
        self.lexer = Lexer(code)
        self.parser = Parser(self.lexer)

    def _lex(self):
        self.lexer.lex()

    def _parse(self):
        self.parser.parse()

    def run(self):
        self._lex()
        self._parse()
        print(self.parser.ast.children)

if __name__ == '__main__':
    import plum
    import sys
    filename = sys.argv[1]
    args = plum.get_args({"output": ["-o", "--out"]}, {"output": plum.String(None)})
    compiler = Compiler(file=filename)
    compiler.run()
