# main.py

import sys
from aurora_parser import *

raw_input=input
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            parser = AuroraParser(f_in.read())
            print(parser._lexer.tokenized_code)
            code = ''.join([ item[1] for item in parser._lexer.tokenized_code ])
    else:
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            cmd = sys.stdin.readline().strip()
            if cmd == "quit":
                break

if __name__ == '__main__':
    main()
