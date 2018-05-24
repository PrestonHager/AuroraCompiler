# aurora_lexer.py

from copy import copy

class AuroraLexer:
    def __init__(self, code):
        self.tokenized_code = []
        self.operations = {}
        self.operations_2 = {}
        with open("operations.txt", 'r') as f_in:
            for line in f_in.read().strip().split("\n"):
                if len(line.split(":=")) > 1:
                    self.operations[line.split(":=")[0]] = ''.join(line.split(":=")[1:])
                elif len(line.split("=:")) > 1:
                    self.operations_2[line.split("=:")[0]] = ''.join(line.split("=:")[1:])
        for key in self.operations_2:
            characters = self.operations_2[key]
            in_set = False
            set = []
            new_characters = []
            for char in characters:
                if in_set and char != "-":
                    set.append(char)
                if char == "]":
                    in_set = False
                    new_characters += [chr(i) for i in range(ord(set[0]), ord(set[1])+1)]
                    set = []
                    continue
                if char == "[":
                    in_set = True
                if not in_set:
                    new_characters.append(char)
            self.operations_2[key] = new_characters
        self.operation_keys = sorted(self.operations, key=lambda k: len(self.operations[k]), reverse=True)
        self._lex(code)

    def _lex(self, code):
        current_id = ""
        index = -1
        position = [0, 1]
        in_comment = False
        in_string = False
        in_operation = [False, "", ""]
        while index < len(code)-1:
            index += 1
            position[0] += 1
            if code[index] == "\n":
                if in_comment:
                    in_comment = False
                    self.tokenized_code.append(["ID", current_id, copy(position)])
                    current_id = ""
                position[1] += 1
                position[0] = 0
                continue
            if in_operation[0]:
                if code[index] in in_operation[1]:
                    current_id += code[index]
                    continue
                else:
                    self.tokenized_code.append([in_operation[2], current_id, copy(position)])
                    current_id = ""
                    in_operation = [False, "", ""]
            if in_comment:
                current_id += code[index]
                continue
            if in_string:
                if code[index] == "\"":
                    in_string = False
                    self.tokenized_code.append(["ID", current_id, copy(position)])
                    current_id = ""
                    self.tokenized_code.append(["END_STRING_DEF", "\"", copy(position)])
                    continue
                else:
                    current_id += code[index]
                    continue
            continue_loop = False
            for key in self.operation_keys:
                operation = self.operations[key]
                if ''.join(code[index:index+len(operation)]) == operation:
                    if current_id != "":
                        self.tokenized_code.append(["ID", current_id, copy(position)])
                        current_id = ""
                    self.tokenized_code.append([key, operation, copy(position)])
                    index += len(operation)-1
                    position[0] += len(operation)-1
                    if key == "STRING_DEF":
                        in_string = True
                    if key == "COMMENT":
                        in_comment = True
                    continue_loop = True
                    break
            if continue_loop:
                continue
            for key in self.operations_2:
                characters = self.operations_2[key]
                if code[index] in characters:
                    in_operation = [True, characters, key]
                    current_id = code[index]
                    continue_loop = True
                    break
            if continue_loop:
                continue
            current_id += code[index]
