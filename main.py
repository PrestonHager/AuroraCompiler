# main.py

from aurora_parser import *
import sys

raw_input=input
def main():
    parser = Parser()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            print(parser.parse(f_in.read()))
    else:
        while True:
            cmd = raw_input(">>> ")
            if cmd == "quit":
                break
            print(parser.parse(cmd))

if __name__ == '__main__':
    main()
