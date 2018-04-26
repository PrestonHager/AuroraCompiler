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
        index = -1
        position = [-1, 0]
        in_comment = False
        in_string = False
        while index < len(code)-1:
            index += 1
            position[0] += 1
            if code[index] == "\n":
                position[1] += 1
                position[0] = 0
                if in_comment:
                    in_comment = False
                    self.tokenized_code.append(("ID", current_id, copy(position)))
                continue
            if in_comment:
                current_id += code[index]
                continue
            if in_string:
                if code[index] == "\"":
                    self.tokenized_code.append(("ID", current_id, copy(position)))
                    current_id = ""
                else:
                    current_id += code[index]
                    continue
            continue_loop = False
            for key in self.operation_keys:
                operation = self.operations[key]
                if ''.join(code[index:index+len(operation)]) == operation:
                    if current_id != "":
                        self.tokenized_code.append(("ID", current_id, copy(position)))
                        current_id = ""
                    self.tokenized_code.append((key, operation, copy(position)))
                    index += len(operation)
                    position[0] += len(operation)
                    if key == "STRING_DEF":
                        in_string = True
                    if key == "COMMENT":
                        in_comment = True
                    break
                    continue_loop = True
            if continue_loop:
                continue
            current_id += code[index]
