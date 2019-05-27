# lexer.py
# by Preston Hager
# for Aurora Compiler

from copy import copy
from re import compile

class Lexer:
    # some regex constants
    number_regex = compile(r'[0-9]+')
    float_regex = compile(r'[0-9]*\\.[0-9]+')
    hex_number_regex = compile(r'0x[0-9]+')

    def __init__(self, code, bin_dir):
        """
        Creates a new Lexer instance

        Parameters
        ----------
        code : str
            Input code as a string.
        bin_dir : str
            Directory of the folder that contains the bin folder that `compiler.py` is in.

        Returns
        -------
        Lexer
            New Lexer instance with previous parameters.
        """
        # Store the bin_dir for the Parser cuz we're nice ;)
        self.bin_dir = bin_dir
        # Define class variables
        self.code = code.strip()+"\n"
        self.lexed_code = []
        # open the operations.txt file and read and put them into a dictionary.
        with open(bin_dir+"/operations.txt", 'r') as f_in:
            cont = f_in.read().strip()
        self.operations = {l.split(":=")[0].strip(): l.split(":=")[1].strip().replace("\s", " ").replace("\\n", "\n") for l in cont.split("\n") if l.strip() != ""}
        self.operations = {k: self.operations[k] for k in sorted(self.operations, key=lambda k: len(self.operations[k]), reverse=True)}

    def lex(self):
        """
        Lexes or Tokenizes code
        """
        # define a few helpful variables
        index = 0
        token = ""
        token_start = [1, 1]
        current_position = [1, 1]
        # loop over the code until the index has reached the end
        while index < len(self.code):
            # if the token hasn't been started yet, set the token_start variable
            if token == "":
                token_start = copy(current_position)
            # add the character at self.code[index] to the token
            token += self.code[index]
            # loop over each operation we have and check the current index to see if we match that operation.
            for operation in self.operations:
                if self.operations[operation] == ''.join(self.code[index:index+len(self.operations[operation])]):
                    # put the current token in the lexed_code, if there is one
                    if len(token) > 1:
                        if self._check_number(''.join(token[:-1])):
                            self.lexed_code.append(Token("NUMBER", ''.join(token[:-1]), token_start))
                        else:
                            self.lexed_code.append(Token("WORD", ''.join(token[:-1]), token_start))
                    # put the current operation into the lexed_code
                    self.lexed_code.append(Token(operation, self.operations[operation], current_position))
                    # increase the index by the length of the operation-1
                    index += len(self.operations[operation])-1
                    # reset the token variable
                    token = ""
                    # break out of the loop, no point in going over the rest of the operations
                    break
            # increase the current position
            current_position[1] += 1
            # if the character at self.code[index] is a newline character, set the current position differently
            if self.code[index] == "\n":
                current_position = [current_position[0]+1, 1]
            # increase the index
            index += 1
        # if there is still a token that hasn't been added then add it
        if token != "":
            if self._check_number(token):
                self.lexed_code.append(Token("NUMBER", token, token_start))
            else:
                self.lexed_code.append(Token("WORD", token, token_start))

    def _check_number(self, token):
        if self.number_regex.match(token):
            return True
        elif self.float_regex.match(token):
            return True
        elif self.hex_number_regex.match(token):
            return True
        return False

class Token:
    def __init__(self, name, value, position):
        self.name = name
        self.value = value
        self.position = copy(position)

    def __str__(self):
        printable_value = self.value.replace('\n', '\\n')
        return f"<Token {self.name}: `{printable_value}` ({self.position[0]}, {self.position[1]})>"

    def __repr__(self):
        return self.__str__()
