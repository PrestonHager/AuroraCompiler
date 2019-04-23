# compiler.py
# by Preston Hager
# for Aurora Compiler

from utils.lexer import *
from utils.parser import *
from utils.generator import *
from utils.errors import CompilerError

class Compiler:
    def __init__(self, bin_dir, file=None, text=None):
        if file != None:
            with open(file, 'r') as f_in:
                code = f_in.read()
        elif text != None:
            code = text
        else:
            raise Exception("No code input found. Please supply either a file or text.")
        self.lexer = Lexer(code, bin_dir)
        self.parser = Parser(self.lexer)
        self.generator = Generator(self.parser)
        self.success = False

    def _lex(self):
        self.lexer.lex()

    def _parse(self):
        self.parser.parse()

    def _generate(self):
        self.generator.generate()

    def _run(self):
        print("Lexing....")
        self._lex()
        # print(self.lexer.lexed_code)
        print("Parsing....")
        self._parse()
        # print(self.parser.ast.children)
        print("Generating code....")
        self._generate()
        # print(self.generator.generated_code)

    def run(self):
        try:
            self._run()
            self.success = True
        except ParserError as err:
            print(err.__class__.__name__+": "+err.message)
        except Exception as err:
            raise err

    def save(self, filename):
        if self.success:
            print(f"Saving under '{filename}'.")
            with open(filename, 'w') as f_out:
                f_out.write(self.generator.generated_code)
        else:
            raise CompilerError("No successful compilation to save.")

    def assemble(self, filename, output=None):
        if self.success:
            if output == None:
                output = '.'.join(filename.split(".")[:-1])+".bin"
            print(f"Assembling '{filename}'.")
            os.system(f"nasm -f bin -o {output} {filename}")
        else:
            raise CompilerError("No successful compilation to assemble.")

if __name__ == '__main__':
    import os
    import plum
    import sys
    if len(sys.argv) <= 1:
        print("Missing input file.")
        exit()
    filename = sys.argv[1]
    filepath = os.path.split(filename)
    build_dir = os.path.join(*filepath[:-1], "build")
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    outloc = os.path.join(*filepath[:-1], "build", ''.join(filepath[-1].split(".")[:-1]))
    bin_dir = os.path.join(*os.path.split(os.path.dirname(os.path.abspath(__file__)))[:-1])
    args = plum.get_args({"output": ["-o", "--out"]}, {"output": plum.String(outloc)})
    compiler = Compiler(bin_dir, file=filename)
    compiler.run()
    if compiler.success:
        compiler.save(args["output"]+".asm")
        # compiler.assemble(args["output"]+".asm", args["output"]+".bin")
        # os.remove(args["output"]+".asm")
