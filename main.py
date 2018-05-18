# main.py

import sys
from aurora_generator import *

raw_input=input
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            generator = AuroraGenerator(f_in.read())
            print(generator._parser._lexer.tokenized_code)
            print(generator._parser.parsed_code)
            print(generator.generated_code)
            code = ''.join([ item[1] for item in generator._parser._lexer.tokenized_code ])
    else:
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            cmd = sys.stdin.readline().strip()
            if cmd == "quit":
                break

if __name__ == '__main__':
    main()
