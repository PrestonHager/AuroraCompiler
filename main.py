# main.py

import sys
from aurora_lexer import *

raw_input=input
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            print(AuroraLexer(f_in.read()).tokenized_code)
    else:
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            cmd = sys.stdin.readline().strip()
            if cmd == "quit":
                break

if __name__ == '__main__':
    main()
