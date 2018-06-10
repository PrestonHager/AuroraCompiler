# compiler.py

import sys
from aurora_generator import *
import traceback
import os
import subprocess

raw_input=input
def main():
    if not os.path.exists("./build/"):
        os.makedirs("./build/")
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            generator = AuroraGenerator(f_in.read())
            print(generator._parser._lexer.tokenized_code)
            print(generator._parser.parsed_code)
            filename = "./build/" + os.path.basename(sys.argv[1]).strip(".aurora") + ".py"
            with open(filename, 'w') as f_out:
                f_out.write(generator.generated_code)
            if "-r" in sys.argv or "--run" in sys.argv:
                try:
                    subprocess.call(["python", filename])
                except:
                    traceback.print_exc()
    else:
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            cmd = sys.stdin.readline().strip()
            if cmd == "quit":
                break
            generator = AuroraGenerator(cmd)
            try:
                exec(generator.generated_code)
            except Exception:
                traceback.print_exc()

if __name__ == '__main__':
    main()
