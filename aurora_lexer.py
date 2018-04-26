# aurora_lexer.py

from copy import copy

class AuroraLexer:
    def __init__(self, code):
        self.tokenized_code = []
        self.operations = {}
        with open("operations.txt", 'r') as f_in:
            for line in f_in.read().split("\n"):
                self.operations[line.split(":=")[0]] = ''.join(line.split(":=")[1:])
        self.operation_keys = sorted(self.operations, key=lambda k: len(self.operations[k]), reverse=True)
        self._lex(code)

    def _lex(self, code):
        current_id = ""
        index = 0
        position = [0, 0]
        while index < len(code):
            for key in self.operation_keys:
                operation = self.operations[key]
                if ''.join(code[index:index+len(operation)]) == operation:
                    self.tokenized_code.append((key, operation, copy(position)))
                    index += len(operation)
                    position[0] += len(operation)
                    break
            if code[index] == "\n":
                position[1] += 1
                position[0] = -1
            index += 1
            position[0] += 1