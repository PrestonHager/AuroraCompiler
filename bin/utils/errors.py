# errors.py
# by Preston Hager
# for Aurora Compiler

class ParserError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class CompilerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

__all__ = ["CompilerError", "ParserError"]
