# aurora_parser.py

from aurora_lexer import AuroraLexer

class AuroraParser:
    # initialization of the Parser.
    def __init__(self, code):
        # takes the same input as the lexer, because it is lexered in this class
        self._lexer = AuroraLexer(code)
        # default values
        self.parsed_code = {"body": [], "initialized": {"all": [], "import": [], "defined": [], "required": []}}
        self.token_index = 0
        self._parse()

    # the accept function, tests for a token id at a token index
    def _accept(self, token_id, token_index):
        # this makes comparisons a lot shorter to type, and helps with error handlering a little
        # if the token index is more than the length of the tokenized code then it's false
        if token_index >= len(self._lexer.tokenized_code):
            return False
        # otherwise, if the token id at the index of the token index of the tokenized code is equal to the token id then true
        if self._lexer.tokenized_code[token_index][0] == token_id:
            return True
        return False

    # the accept function, tests for a token id at a token index for a certain depth
    def _expect(self, token_id, max_depth, token_index):
        index = 0
        # while the index is less than the max depth, or if the max depth is 1, and the index is less than the length of the tokenized code
        while index < max_depth or max_depth == -1 and index < len(self._lexer.tokenized_code):
            # just like accept, if the character at the index of the tokenized code is equal to the token id then true
            if self._lexer.tokenized_code[token_index+index][0] == token_id:
                return True
            index += 1      # increment the index by one
        # if any of the while loop conditions failed then it's false
        return False

    # the add variable adds to the initialized dictionary of the parsed code
    def _add_variable(self, var, section):
        if var not in self.parsed_code["initialized"][section]:
            self.parsed_code["initialized"][section].append(var)

    # the statment function, takes a token index for an input, and returns a token in a AST format used for beginings of statments
    def _statement(self, token_index):
        if self._accept("COMMENT", token_index):
            if self._accept("ID", token_index+1):
                id = self._lexer.tokenized_code[token_index+1][1]
                self.token_index += 1
                return self._create_new_token("comment", id)
        if self._accept("STRING_TYPE", token_index):
            if self._expect("ASIGN", 1, token_index+1):
                if self._expect("VARIABLE", 1, token_index+2):
                    id = self._lexer.tokenized_code[token_index+2][1]
                    self._add_variable(id, "all")
                    self._add_variable(id, "defined")
                    self._add_variable("string_variables", "required")
                    if self._expect("VALUE", 1, token_index+3):
                        variable_value = self._expression(token_index+4)
                        return self._create_new_token("string_variable", id, [variable_value])
                    else:
                        return self._create_new_token("string_variable", id)
        if self._accept("NUMBER_TYPE", token_index):
            if self._expect("ASIGN", 1, token_index+1):
                if self._expect("VARIABLE", 1, token_index+2):
                    id = self._lexer.tokenized_code[token_index+2][1]
                    self._add_variable(id, "all")
                    self._add_variable(id, "defined")
                    self._add_variable("number_variables", "required")
                    if self._expect("VALUE", 1, token_index+3):
                        variable_value = self._expression(token_index+4)
                        return self._create_new_token("number_variable", id, [variable_value])
                    else:
                        return self._create_new_token("number_variable", id)
        if self._accept("VARIABLE", token_index):
            id = self._lexer.tokenized_code[token_index][1]
            self._add_variable(id, "all")
            if self._expect("FUNC", 1, token_index+1):
                self._add_variable(id, "import")
                arguments = []
                arg_num = 0
                while True:
                    arg = self._expression(token_index + 2 + arg_num)
                    if arg != False:
                        arguments.append(arg)
                        arg_num += 1
                    else:
                        break
                self.token_index += 1 + len(arguments)
                return self._create_new_token("function", id, arguments)
        return False

    # the expression function, input of a token index, output of a token in AST format, used for strings, numbers, and ids
    def _expression(self, token_index):
        if self._accept("STRING_DEF", token_index):
            if self._expect("END_STRING_DEF", 2, token_index+1):
                id = self._lexer.tokenized_code[token_index+1][1]
                return self._create_new_token("string", id)
        if self._accept("NUMBER", token_index):
            number = self._lexer.tokenized_code[token_index][1]
            return self._create_new_token("number", number)
        if self._accept("VARIABLE", token_index):
            variable = self._lexer.tokenized_code[token_index][1]
            arguments = []
            arg_num = 1
            while True:
                arg = self._expression(token_index + arg_num*2)
                if arg != False:
                    arguments.append(arg)
                    arg_num += 1
                else:
                    break
            return self._create_new_token("variable", variable, arguments)
        if self._accept("ID", token_index):
            id = self._lexer.tokenized_code[token_index][1]
            return self._create_new_token("id", id)
        return False

    # the create new token funciton, input of a type, value, and children tokens, and output of token (dictionary)
    def _create_new_token(self, type, value="", children=[]):
        new_token = {"token_type": type, "token_value": value, "children": children}
        return new_token

    # parse the code
    def _parse(self):
        # while the current token index is less than the length of the tokenized code
        while self.token_index < len(self._lexer.tokenized_code):
            # create a statment at that index
            statement = self._statement(self.token_index)
            if statement != False: # if it's not false, then add it to the parsed code body
                self.parsed_code["body"].append(statement)
            # and increment the token index by one
            self.token_index += 1
