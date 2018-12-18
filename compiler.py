# compiler.py
# by Preston Hager
# for Aurora Compiler

from utils.lexer import *
from utils.parser import *
from utils.generator import *

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
        self.generator = Generator(self.parser)

    def _lex(self):
        self.lexer.lex()

    def _parse(self):
        self.parser.parse()

    def _generate(self):
        self.generator.generate()

    def run(self):
        self._lex()
        # print(self.lexer.lexed_code)
        self._parse()
        # print(self.parser.ast.children)
        self._generate()
        # print(self.generator.generated_code)

    def save(self, filename):
        with open(filename, 'w') as f_out:
            f_out.write(self.generator.generated_code)

if __name__ == '__main__':
    import os
    import plum
    import sys
    filename = sys.argv[1]
    filepath = os.path.split(filename)
    build_dir = os.path.join(*filepath[:-1], "build")
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    outloc = os.path.join(*filepath[:-1], "build", ''.join(filepath[-1].split(".")[:-1])+".asm")
    args = plum.get_args({"output": ["-o", "--out"]}, {"output": plum.String(outloc)})
    compiler = Compiler(file=filename)
    compiler.run()
    compiler.save(args["output"])
