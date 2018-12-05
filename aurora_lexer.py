# aurora_lexer.py

# import statements
import re
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
                    # format, replace curly brackets: {TOKEN_NAME}=:{regex}
                    # put the pair into self.operations_2
                    # this is a regex match to any given section
                    self.operations_2[line.split("=:")[0]] = re.compile(''.join(line.split("=:")[1:]))
        # sort the operations by length of the value into a variable
        self.operation_keys = sorted(self.operations, key=lambda k: len(self.operations[k]), reverse=True)
        self._lex(code) # and the "lex" or "tokenize" the code

    def _lex(self, code):
        # initalize variables to default values
        current_id = ""
        index = -1
        position = [0, 1]
        in_comment = False
        # while the index is less than the length of the code then...
        while index < len(code)-1:
            index += 1 # increment index
            position[0] += 1 # increment position (used for the position of the token)
            if code[index] == "\n": # if the character at index is a newline
                if current_id != "":
                    regex_op = self._check_regex_operations(current_id)
                    if regex_op:
                        self.tokenized_code.append([regex_op, current_id, copy(position)])
                    else:
                        self.tokenized_code.append(["ID", current_id, copy(position)])
                    current_id = ""
                # set the in comment to false, as it expires after a new line
                in_comment = False
                # the position will be changed to x=0, y+=1
                position[1] += 1
                position[0] = 0
                continue
            # if still in a comment, then just add to the current id and move on
            if in_comment:
                current_id += code[index]
                continue
            # now to detect whether a character (or range of characters) is in the operations
            continue_loop = False # this is set to true to continue to the next index, if a success happens
            # for each key in the operations
            for key in self.operation_keys:
                operation = self.operations[key]
                # if the character's between index and index+length of operation is equal to the operation
                if ''.join(code[index:index+len(operation)]) == operation:
                    # add current_id to tokenized_code if there is one
                    if current_id != "":
                        regex_op = self._check_regex_operations(current_id)
                        if regex_op:
                            self.tokenized_code.append([regex_op, current_id, copy(position)])
                        else:
                            self.tokenized_code.append(["ID", current_id, copy(position)])
                    current_id = ""
                    # test for the operation as a comment
                    if key == "COMMENT":
                        in_comment = True
                    # add the operation token to the tokenized_code
                    self.tokenized_code.append([key, operation.strip(), copy(position)])
                    # adjust the index and position variables
                    index += len(operation)-1
                    position[0] += len(operation)-1
                    continue_loop = True # and continue the loop after breaking out of the for loop
                    break
            if continue_loop:
                continue
            # if non of the above has worked (the character wasn't in any of the operations), then add it to the current_id
            # it will be added to the tokenized_code the next time an operation is found
            current_id += code[index]
        # at the end, an operation from operations_2 might still be, so add that
        if current_id != "":
            regex_op = self._check_regex_operations(current_id)
            if regex_op:
                self.tokenized_code.append([regex_op, current_id, copy(position)])
            else:
                self.tokenized_code.append(["ID", current_id, copy(position)])

    def _check_regex_operations(self, current_id):
        # see if the current amount matches any regex in operations_2
        for key in self.operations_2:
            # test for the current id matching the regex
            if self.operations_2[key].match(current_id):
                # if it does match, then set in_operation to true.
                return key
