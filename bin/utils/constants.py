# constants.py
# by Preston Hager
# for Aurora Compiler

# for compiler.py, the help message
HELP_MESSAGE = """Usage: aurora [file] [options...]

    --out (-o)              output file.
    --freestanding (-fs)    copy the library files to the compilation spot.
    --help (-h)             display this help message.
    --no-compile-dependencies (-cd) don't compile the aurora files that this one depends on."""

# These are for the infix to postfix thing.
OPERATIONS = {
    "EXPONENT": 4,
    "TIMES": 3,
    "DIVIDE": 3,
    "PLUS": 2,
    "MINUS": 2
}

# for generator.py, comparison jump instructions
COMPARISON_INSTRUCTIONS = {
    "EQUALS_TEST": "je",
    "NOT_EQUAL_TEST": "jne",
    "LESS_THAN_TEST": "jl",
    "LESS_THAN_EQUAL_TEST": "jle",
    "GREATER_THAN_TEST": "jg",
    "GREATER_THAN_EQUAL_TEST": "jge"
}
