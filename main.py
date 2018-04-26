# main.py

import sys

raw_input=input
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            f_in.read()
    else:
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            cmd = sys.stdin.readline().strip()
            if cmd == "quit":
                break

if __name__ == '__main__':
    main()
