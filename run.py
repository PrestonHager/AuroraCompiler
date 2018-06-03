# run.py

import sys
import traceback
import os.path

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f_in:
            try:
                exec(f_in.read())
            except:
                traceback.print_exc()
    else:
        print("You must specify a file to run it.")

if __name__ == '__main__':
    main()
