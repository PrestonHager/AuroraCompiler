# main.py

import sys
from aurora_generator import *

raw_input=input
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            generator = AuroraGenerator(f_in.read())
            with open(sys.argv[1].strip(".aurora") + ".py", 'w') as f_out:
                f_out.write(generator.generated_code)
            print(generator.generated_code)
    else:
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            cmd = sys.stdin.readline().strip()
            if cmd == "quit":
                break

if __name__ == '__main__':
    main()
