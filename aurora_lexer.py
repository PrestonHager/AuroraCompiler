# aurora_lexer.py

# import statements
from copy import copy

class AuroraLexer:
    # initalization of the Lexer.
    def __init__(self, code):
        # takes the input of Aurora formated code.
        self.tokenized_code = [] # set all variables to "empty"
        self.operations = {}
        self.operations_2 = {}
        # open the operations file to get operation tokens
        with open("operations.txt", 'r') as f_in:
            # for each line in the file.
            for line in f_in.read().strip().split("\n"):
                # Two formats, one for literal character, one for regex like.
                if len(line.split(":=")) > 1: # literal character format
                    # format, replace square brackets: [TOKEN_NAME]:=[character string]
                    # put the pair into self.operations.
                    self.operations[line.split(":=")[0]] = ''.join(line.split(":=")[1:]).replace("\\s", " ")
                elif len(line.split("=:")) > 1: # regex like format
                    # format, replace curly brackets: {TOKEN_NAME}=:{literal character string}[{characters that can be repeated}]
                    # put the pair into self.operations_2
                    self.operations_2[line.split("=:")[0]] = ''.join(line.split("=:")[1:])
        # reformat the pairs in operations_2 so that the python code can read it.
        # for each key in operations_2
        for key in self.operations_2:
            characters = self.operations_2[key]     # get all the characters.
            in_set = False                          # in_set is the square brackets, characters that can be repeated
            set = []                                # set of letters defaults to "empty"
            new_characters = []                     # the new_characters is the "output" of this
            # for character in the string of character for the pair
            for char in characters:
                if in_set and char != "-": # if in a set and the character isn't "thru" then append to set.
                    set.append(char)
                if char == "]": # if the character is "set finish" then finsih the set and append to new_characters
                    in_set = False
                    new_characters += [chr(i) for i in range(ord(set[0]), ord(set[1])+1)]
                    set = []
                    continue
                if char == "[": # if the character is "set start" set in_set to true.
                    in_set = True
                if not in_set: # if still not in set, then append the character to new_characters
                    new_characters.append(char)
            # set the new characters to the operation.
            self.operations_2[key] = new_characters
        # sort the operations into a variable
        self.operation_keys = sorted(self.operations, key=lambda k: len(self.operations[k]), reverse=True)
        self._lex(code) # and the "lex" or "tokenize" the code

    def _lex(self, code):
        # initalize variables to default values
        current_id = ""
        index = -1
        position = [0, 1]
        in_comment = False
        in_string = False
        in_operation = [False, "", ""]
        # while the index is less than the length of the code then...
        while index < len(code)-1:
            index += 1 # increment index
            position[0] += 1 # increment position (used for the position of the token)
            if code[index] == "\n": # if the character at index is a newline
                if in_comment: # commnets can be added to tokenized_code and reset
                    in_comment = False
                    self.tokenized_code.append(["ID", current_id, copy(position)])
                    current_id = ""
                # the position will be changed to x=0, y+=1
                position[1] += 1
                position[0] = 0
                continue
            if in_operation[0]: # if in and operation (the operations_2 values)
                if code[index] in in_operation[1]: # if the character at index is in the set
                    # the current_id += the character
                    current_id += code[index]
                    continue
                else: # otherwise, the current_id will be added to the tokenized_code
                    self.tokenized_code.append([in_operation[2], current_id, copy(position)])
                    current_id = "" # reset current_id and in_operation
                    in_operation = [False, "", ""]
            if in_comment: # if in a comment then just add the current_id
                current_id += code[index]
                continue
            if in_string: # if in a string then
                if code[index] == "\"": # add the current_id to the tokenized_code if an end string
                    in_string = False
                    self.tokenized_code.append(["ID", current_id, copy(position)])
                    current_id = ""
                    self.tokenized_code.append(["END_STRING_DEF", "\"", copy(position)])
                    continue
                else: # otherwise add to the current_id
                    current_id += code[index]
                    continue
            continue_loop = False
            for key in self.operation_keys:
                operation = self.operations[key]
                if ''.join(code[index:index+len(operation)]) == operation:
                    if current_id != "":
                        self.tokenized_code.append(["ID", current_id, copy(position)])
                        current_id = ""
                    self.tokenized_code.append([self._strip_numbers(key), operation, copy(position)])
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
        if current_id != "" and in_operation[0]:
            self.tokenized_code.append([in_operation[2], current_id, copy(position)])
        elif current_id != "":
            self.tokenized_code.append(["ID", current_id, copy(position)])

    def _strip_numbers(self, string):
        while string[-1] in "0123456789":
            for num in "0123456789":
                string = string.strip(num)
        return string
