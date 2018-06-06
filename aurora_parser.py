# aurora_parser.py

# import statements
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
    def _expect(self, token_id, max_depth, token_index, msg=""):
        index = 0
        # while the index is less than the max depth, or if the max depth is 1, and the index is less than the length of the tokenized code
        while (index < max_depth or max_depth == -1) and index < len(self._lexer.tokenized_code):
            print(self._lexer.tokenized_code)
            # just like accept, if the character at the index of the tokenized code is equal to the token id then true
            if self._lexer.tokenized_code[token_index+index][0] == token_id:
                return True
            index += 1      # increment the index by one
        # if any of the while loop conditions failed then it's false
        # if it is false, then there is a syntax error.
        raise SyntaxError(msg+" At {position} from {area}".format(position=', '.join([str(p) for p in self._lexer.tokenized_code[token_index][2]]), area=''.join([t[1] for t in self._lexer.tokenized_code[token_index-2:token_index+1]])))
        return False

    # the add variable adds to the initialized dictionary of the parsed code
    def _add_variable(self, var, section):
        if var not in self.parsed_code["initialized"][section]:
            self.parsed_code["initialized"][section].append(var)

    # the statment function, takes a token index for an input, and returns a token in a AST format used for beginings of statments
    def _statement(self, token_index):
        used_index = 1 # set used index to 1, this is so that funcitons can be nested
        created_token = False
        # look for comments
        if self._accept("COMMENT", token_index):
            if self._accept("ID", token_index+1): # an id must come after a comment
                # get the id and return a new "comment" token
                id = self._lexer.tokenized_code[token_index+1][1]
                used_index = 2
                created_token = self._create_new_token("comment", id)
        # look for funciton definitions
        elif self._accept("FUNC_TYPE", token_index):
            if self._expect("ASIGN", 1, token_index+1, "Expected ':' after function decleration."):
                if self._expect("VARIABLE", 1, token_index+2, "Expected varaible after function decleration."):
                    id = self._lexer.tokenized_code[token_index+2][1]
                    self._add_variable(id, "all")
                    self._add_variable(id, "defined")
                    if self._expect("FUNC", 1, token_index+3, "Expected '>' after function name."):
                        # check for an end tag after function decleration
                        self._expect("END", -1, token_index+2, "Expected 'end' tag after function decleration.")
                        arguments = []
                        arg_used_index = 0
                        while True:
                            if self._accept("VARIABLE", token_index+4+arg_used_index):
                                variable = self._lexer.tokenized_code[token_index+4+arg_used_index][1]
                                if self._expect("TYPE", 1, token_index+4+arg_used_index+1, "Expected '::' after variable decleration in function arguments."):
                                    if self._accept("STRING_TYPE", token_index+4+arg_used_index+2):
                                        if self._accept("VALUE", token_index+4+arg_used_index+3):
                                            value = self._expression(token_index+4+arg_used_index+3)
                                            arg_used_index += 4 + value[0]
                                            arguments.append(self._create_new_token("string_variable", variable, [value[1]]))
                                        else:
                                            arg_used_index += 4
                                            arguments.append(self._create_new_token("string_variable", variable))
                                    elif self._accept("NUMBER_TYPE", token_index+4+arg_used_index+2):
                                        if self._accpet("VALUE", token_index+4+arg_used_index+3):
                                            value = self._expression(token_index+4+arg_used_index+3)
                                            arg_used_index += 4 + value[0]
                                            arguments.append(self._create_new_token("number_variable", variable, [value[1]]))
                                        else:
                                            arg_used_index += 4
                                            arguments.append(self._create_new_token("number_variable", variable))
                            else:
                                break
                        if self._expect("RETURN_TYPE", 1, token_index+3+arg_used_index, "Expected '=>' after function argument list."):
                            if self._accept("STRING_TYPE", token_index+3+arg_used_index+1):
                                return_type = "string"
                            elif self._accept("NUMBER_TYPE", token_index+3+arg_used_index+1):
                                return_type = "number"
                            elif self._accept("VOID_TYPE", token_index+3+arg_used_index+1):
                                return_type = "void"
                            else:
                                self._expect("", 0, token_index+3+arg_used_index+1, "Expected return type after function decleration.")
                            inner_code = []
                            statement = self._statement(token_index+3+arg_used_index+2)
                            while True:
                                if statement[1] != False:
                                    inner_code.append(statement[1])
                                arg_used_index += statement[0]
                                statement = self._statement(token_index+3+arg_used_index+2)
                                if statement[1] != False and statement[1]["token_type"] == "end":
                                    break
                            used_index = 4 + arg_used_index
                            created_token = self._create_new_token("function_definition", id, [self._create_new_token("arguments", "", arguments), self._create_new_token("return_type", return_type), self._create_new_token("code", "", inner_code)])
        elif self._accept("END", token_index):
            created_token = self._create_new_token("end")
        # look for string definitions
        elif self._accept("STRING_TYPE", token_index):
            # format is: `String: var = "value"` or STRING_TYPE + ASIGN + VARIABLE + VALUE + (EXPRESSION)
            if self._expect("ASIGN", 1, token_index+1, "Expected ':' after String variable definition."):
                if self._expect("VARIABLE", 1, token_index+2, "Expected varaible name after String variable definition."):
                    # get the variable name (id) and add it to initalized varaibles
                    id = self._lexer.tokenized_code[token_index+2][1]
                    self._add_variable(id, "all")
                    self._add_variable(id, "defined")
                    self._add_variable("string_variables", "required")
                    # if the variable is preset, then it has a value token
                    if self._accept("VALUE", token_index+3):
                        variable_value = self._expression(token_index+4)
                        used_index = 5
                        created_token = self._create_new_token("string_variable", id, [variable_value[1]])
                    # otherwise, it's not preset, and just initialized with a void value
                    else:
                        used_index = 3
                        created_token = self._create_new_token("string_variable", id)
        # look for number definitions
        elif self._accept("NUMBER_TYPE", token_index):
            # similar to string definitions: `Number: var = 15` or NUMBER_TYPE + ASIGN + VARIABLE + VALUE + (EXPRESSION)
            if self._expect("ASIGN", 1, token_index+1, "Expected ':' after Number variable definition."):
                if self._expect("VARIABLE", 1, token_index+2, "Expected variable name after Number variable definition."):
                    # get the variable name (id)
                    id = self._lexer.tokenized_code[token_index+2][1]
                    self._add_variable(id, "all")
                    self._add_variable(id, "defined")
                    self._add_variable("number_variables", "required")
                    # if the variable is set then get the value and return a created token
                    if self._accept("VALUE", token_index+3):
                        variable_value = self._expression(token_index+4)
                        used_index = 5
                        created_token = self._create_new_token("number_variable", id, [variable_value[1]])
                    # otherwise return a created token with no preset variable value
                    else:
                        used_index = 3
                        created_token = self._create_new_token("number_variable", id)
        # look for function calls
        elif self._accept("VARIABLE", token_index):
            # format: `function_name>arguments` or VARIABLE + FUNC + (EXPRESSION(S))
            id = self._lexer.tokenized_code[token_index][1] # get variable name
            self._add_variable(id, "all")
            # if a FUNC token, `>`, is found then create a token with children of the following expressions (arguments)
            if self._expect("FUNC", 1, token_index+1):
                self._add_variable(id, "import")
                arguments = [] # set the list (children) of arguments to "empty"
                # get the first argument, as it doesn't require a comma before
                arg = self._expression(token_index + 2)
                if arg[1] != False: # if the argument isn't false,
                    arguments.append(arg[1]) # append the argument to the list
                    arg_used_index = arg[0] # and make the used index equal the used index from the expression
                    while True: # while infinite, a not found argument will break the loop
                        if self._accept("ARGUMENT_SEPERATOR", token_index + 2 + arg_used_index):
                            arg_used_index += 1
                            arg = self._expression(token_index + 2 + arg_used_index) # get the next expression (skip over commas)
                            if arg[1] != False:
                                arguments.append(arg[1])
                                arg_used_index += arg[0]
                            else: # if the argument is false, then break from loop
                                break
                        else:
                            break
                    # make sure the used index is set
                    used_index = 2 + arg_used_index
                    created_token = self._create_new_token("function", id, arguments) # return the created token
            else:
                created_token = self._create_new_token("variable", id)
        # return the created_token and used_index
        return [used_index, created_token]

    # the expression function, input of a token index, output of a token in AST format, used for strings, numbers, and ids
    def _expression(self, token_index):
        used_index = 1
        created_token = False
        # find negivite numbers: `-15`, MINUS + NUMBER
        if self._accept("MINUS", token_index):
            if self._accept("NUMBER", token_index+1):
                self._add_variable("number_variables", "required")
                number = self._lexer.tokenized_code[token_index+1][1]
                used_index = 2
                created_token = self._create_new_token("number", "-"+number)
        # find strings: `"string value"`, STRING_DEF + ID + END_STRING_DEF
        elif self._accept("STRING_DEF", token_index):
            if self._expect("END_STRING_DEF", 2, token_index+1):
                self._add_variable("string_variables", "required")
                id = self._lexer.tokenized_code[token_index+1][1]
                used_index = 3
                created_token = self._create_new_token("string", id) # return created token
        # find numbers: `15`, NUMBER
        elif self._accept("NUMBER", token_index):
            self._add_variable("number_variables", "required")
            number = self._lexer.tokenized_code[token_index][1]
            used_index = 1
            created_token = self._create_new_token("number", number) # return the found token value as an AST token
        # find varaibles, and function call varaibles
        elif self._accept("VARIABLE", token_index):
            variable = self._lexer.tokenized_code[token_index][1]
            # find function call varaibles: `var>arguemnts`, VARIABLE + FUNC + (EXPRESSIONS(s))
            if self._accept("FUNC", token_index+1):
                arguments = [] # set the list (children) of arguments to "empty"
                # get the first argument, as it doesn't require a comma before
                arg = self._expression(token_index + 2)
                if arg[1] != False: # if the argument isn't false,
                    arguments.append(arg[1]) # append the argument to the list
                    arg_used_index = arg[0] # and make the used index equal the used index from the expression
                    while True: # while infinite, a not found argument will break the loop
                        if self._accept("ARGUMENT_SEPERATOR", token_index + 2 + arg_used_index):
                            arg_used_index += 1
                            arg = self._expression(token_index + 2 + arg_used_index) # get the next expression (skip over commas)
                            if arg[1] != False:
                                arguments.append(arg[1])
                                arg_used_index += arg[0]
                            else: # if the argument is false, then break from loop
                                break
                        else:
                            break
                    # make sure the used index is set
                    used_index = 2 + arg_used_index
                created_token = self._create_new_token("function", variable, arguments)
            elif self._accept("OBJ", token_index+1):
                id = self._expression(token_index + 2)
                used_index = 2 + id[0]
                created_token = self._create_new_token("variable", variable, [id[1]])
            else:
                used_index = 1
                created_token = self._create_new_token("variable", variable)
        # find return statement
        elif self._accept("RETURN", token_index):
            id = self._statement(token_index+1)
            used_index = 1 + id[0]
            created_token = self._create_new_token("return", "return", [id[1]])
        # if none of the above, but still an id, return that id
        elif self._accept("ID", token_index):
            id = self._lexer.tokenized_code[token_index][1]
            used_index = 1
            created_token = self._create_new_token("id", id)
        if self._accept("PLUS", token_index+1):
            number2 = self._expression(token_index+2)
            used_index += 1 + number2[0]
            created_token = self._create_new_token("plus", "+", [created_token, number2[1]])
        elif self._accept("MINUS", token_index+1):
            number2 = self._expression(token_index+2)
            used_index += 1 + number2[0]
            created_token = self._create_new_token("subtract", "-", [created_token, number2[1]])
        elif self._accept("MULTIPLY", token_index+1):
            number2 = self._expression(token_index+2)
            used_index += 1 + number2[0]
            created_token = self._create_new_token("multiply", "*", [created_token, number2[1]])
        elif self._accept("DIVIDE", token_index+1):
            number2 = self._expression(token_index+2)
            used_index += 1 + number2[0]
            created_token = self._create_new_token("divide", "/", [created_token, number2[1]])
        return (used_index, created_token)

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
            if statement[1] != False: # if it's not false, then add it to the parsed code body
                self.parsed_code["body"].append(statement[1])
            # and increment the token index by one
            self.token_index += statement[0]
