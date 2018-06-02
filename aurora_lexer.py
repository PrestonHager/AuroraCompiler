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
        # sort the operations by length of the value into a variable
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
            # now to detect whether a character (or range of characters) is in the operations
            continue_loop = False # this is set to true to continue to the next index, if a success happens
            # for each key in the operations
            for key in self.operation_keys:
                operation = self.operations[key]
                # if the character's between index and index+length of operation is equal to the operation
                if ''.join(code[index:index+len(operation)]) == operation:
                    # add current_id to tokenized_code if there is one
                    if current_id != "":
                        self.tokenized_code.append(["ID", current_id, copy(position)])
                        current_id = ""
                    # add the operation token to the tokenized_code
                    self.tokenized_code.append([self.strip_numbers(key), operation.strip(), copy(position)])
                    # adjust the index and position variables
                    index += len(operation)-1
                    position[0] += len(operation)-1
                    # if the operation was a string, or comment set the in_{variable} to true
                    if key == "STRING_DEF":
                        in_string = True
                    if key == "COMMENT":
                        in_comment = True
                    continue_loop = True # and continue the loop after breaking out of the for loop
                    break
            if continue_loop:
                continue
            # for the key in operations_2
            for key in self.operations_2:
                characters = self.operations_2[key]
                # if the current character is in the possible characters then
                if code[index] in characters:
                    # set in_operation to true, and store character, and key(the token name) in the varaible
                    in_operation = [True, characters, key]
                    current_id = code[index] # add the current character to the current_id
                    continue_loop = True # and continue the loop
                    break
            if continue_loop:
                continue
            # if non of the above has worked (the character wasn't in any of the operations), then add it to the current_id
            # it will be added to the tokenized_code the next time an operation is found
            current_id += code[index]
        # at the end, an operation from operations_2 might still be, so add that
        if current_id != "" and in_operation[0]:
            self.tokenized_code.append([in_operation[2], current_id, copy(position)])
        # if not, then the current_id might still be, so add that
        elif current_id != "":
            self.tokenized_code.append(["ID", current_id, copy(position)])

    def strip_numbers(self, string):
        while string[-1].isdigit():
            for n in "0123456789":
                string = string.strip(n)
        return string
