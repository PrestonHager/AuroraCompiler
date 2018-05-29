# Testing for Aurora Compiler

from aurora_generator import AuroraGenerator
import json
import logging
import os
import sys

def main():
    libraries_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "libraries")
    if libraries_dir not in sys.path:
        sys.path.append(libraries_dir)
    logger = logging.getLogger("AuroraTests")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    with open("./tests/tests.json", 'r') as f_in:
        tests = json.load(f_in)
    for test in tests:
        test_logger = logging.getLogger(test["name"])
        test_logger.setLevel(logging.DEBUG)
        test_logger.addHandler(handler)
        test_logger.info("Testing {test}....".format(test=test["name"]))
        with open("./tests/"+test["file"], 'r') as f_in:
            f_con = f_in.read()
        generator = AuroraGenerator(f_con)
        try:
            exec(generator.generated_code)
        except Exception as err:
            test_logger.error("An error occured while trying to execute.")
            test_logger.error("Error: {error}".format(error=err))
        with open("./_aurora_out", 'rb') as f_in:
            test_results = f_in.read().decode('utf-8').strip()
        if test_results == test["output"]:
            test_logger.info("Success! The output matched the given output.")
        else:
            test_logger.info("Failure. The ouput did not match the given ouput.")
            test_logger.info("Given output was:\n{output}".format(output=test["output"]))
            test_logger.info("While the true ouput was:\n{output}".format(output=test_results))
        test_logger.info("Finished.")

if __name__ == '__main__':
    main()
