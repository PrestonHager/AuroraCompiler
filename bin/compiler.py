# compiler.py
# by Preston Hager
# for Aurora Compiler

# Important imports for the lexer, parser, generator, and error handling.
from random import randrange
from utils.lexer import *
from utils.parser import *
from utils.generator import *
from utils.errors import CompilerError
from utils.constants import HELP_MESSAGE

class Compiler:
    def __init__(self, bin_dir, extra, file=None, text=None, is_dependency=False):
        """
        Creates a new Compiler instance

        Parameters
        ----------
        bin_dir : string
            The directory of this file since it contains the utilities and libraries.
        [file] : string
            Path to file containing Aurora code.
        [text] : string
            Or pass in text instead of file path.

        Returns
        -------
        Compiler
            New Compiler instance with previous parameters.
        """
        # each compiler instance get a unique id so that we can include dependencies and do some cool name stuff.
        self.uuid = "%030x" % randrange(16**32)
        if file != None:
            with open(file, 'r') as f_in:
                code = f_in.read()
        elif text != None:
            code = text
        else:
            raise Exception("No code input found. Please supply either a file or text.")
        self.lexer = Lexer(code, bin_dir)
        self.parser = Parser(self.lexer, extra)
        self.generator = Generator(self.parser, self.uuid, is_dependency)
        self.success = False

    def _lex(self):
        self.lexer.lex()

    def _parse(self):
        self.parser.parse()

    def _generate(self):
        self.generator.generate()

    def _run(self):
        self._lex()
        self._parse()
        self._generate()

    def _compile_dependencies(self):
        for file in self.parser.dependencies:
            dependency_compiler = Compiler(self.lexer.bin_dir, self.parser.extra, file[0], is_dependency=True)
            dependency_compiler.run()
            dependency_compiler.save(file[1])

    def run(self):
        """
        Run the compiler to tokenize, parse, and then generate code.
        """
        try:
            self._run()
            if not self.parser.extra["no_compile_dependencies"]:
                self._compile_dependencies()
            self.success = True
        except ParserError as err:
            print(err.__class__.__name__+": "+err.message)
        except Exception as err:
            raise err

    def save(self, filename):
        """
        Save the generated code at a given filepath.

        Parameters
        ----------
        filename : string
            Path or filename of the saved file with generated code.
        """
        if self.success:
            print(f"Saving under '{filename}'.")
            with open(filename, 'w') as f_out:
                f_out.write(self.generator.generated_code)
        else:
            raise CompilerError("No successful compilation to save.")

    def assemble(self, filename, output=None):
        """
        Assemble the generated code into binary bytecode.
        NOTE: Requires NASM

        Parameters
        ----------
        filename : string
            File to take the assembly code from.
        [output] : string
            File to save the bytecode to, if not given it defaults to `filename.bin`.
        """
        if self.success:
            if output == None:
                output = '.'.join(filename.split(".")[:-1])+".bin"
            print(f"Assembling '{filename}'.")
            os.system(f"nasm -f bin -o {output} {filename}")
        else:
            raise CompilerError("No successful compilation to assemble.")

if __name__ == '__main__':
    # Also probably important imports.
    import os
    import plum
    import sys
    # these are arguments that are passed in through the command line. This is just fancy code.
    args = plum.get_args({"output": ["-o", "--out"], "freestanding": ["--freestanding", "-fs"], "no_compile_dependencies": ["--no-compile-dependencies", "-cd"], "help": ["--help", "-h"]}, {"output": plum.String(None)})
    # first check if we should print the help message.
    if args["help"]:
        print(HELP_MESSAGE)
        exit()
    # look for the filename, if it isn't given then we've run into a road-block.
    if len(sys.argv) <= 1:
        print("Missing input file.")
        exit()
    # take the filename and split the path to create a build directory.
    filename = sys.argv[1]
    filepath = os.path.split(filename)
    build_dir = os.path.join(*filepath[:-1], "aurora")
    # oh, yeah, check to see if that directory exists, if not then create it.
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    # we have to have some place to save the file right?
    outloc = os.path.join(*filepath[:-1], "aurora", ''.join(filepath[-1].split(".")[:-1]))
    bin_dir = os.path.join(*os.path.split(os.path.dirname(os.path.abspath(__file__))))
    # Now we get to have fun and create the compiler.
    compiler = Compiler(bin_dir, args, file=filename)
    # and run it. who decided to structure the code like this?
    compiler.run()
    # if the args["output"] is == None, then no default value was passed in and we can use the outloc variable.
    if args["output"] == None:
        args["output"] = outloc
    # check to see if it was actually successful before we try to do stuff to it.
    if compiler.success:
        compiler.save(outloc+".asm")
        compiler.assemble(outloc+".asm", args["output"])
        # os.remove(args["output"]+".asm")
