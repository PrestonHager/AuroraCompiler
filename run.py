# run.py

import sys
import traceback
import os.path

def main():
    libraries_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "libraries")
    if libraries_dir not in sys.path:
        sys.path.append(libraries_dir)
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
