# aurora_parser.py

from aurora_lexer import AuroraLexer

class AuroraParser:
    def __init__(self, code):
        self._lexer = AuroraLexer(code)
        self.parsed_code = {"body": [], "initialized": {"all": [], "import": [], "defined": []}}
        self.token_index = 0
        self._parse()

    def _accept(self, token_id, token_index):
        if token_index >= len(self._lexer.tokenized_code):
            return False
        if self._lexer.tokenized_code[token_index][0] == token_id:
            return True
        return False
    
    def _expect(self, token_id, max_depth, token_index):
        index = 0
        while index < max_depth or max_depth == -1 or index >= len(self._lexer.tokenized_code):
            if self.token_index + index >= len(self._lexer.tokenized_code):
                break
            if self._lexer.tokenized_code[token_index+index][0] == token_id:
                return True
            index += 1
        return False

    def _add_variable(self, var, section):
        if var not in self.parsed_code["initialized"][section]:
            self.parsed_code["initialized"][section].append(var)    
        
    def _statement(self, token_index):
        if self._accept("COMMENT", token_index):
            if self._accept("ID", token_index+1):
                id = self._lexer.tokenized_code[token_index+1][1]
                token_index += 2
                return self._create_new_token("comment", id)
        if self._accept("STRING_TYPE", token_index):
            if self._expect("ASIGN", 1, token_index+1):
                if self._expect("VARIABLE", 1, token_index+2):
                    id = self._lexer.tokenized_code[token_index+2][1]
                    self._add_variable(id, "all")
                    self._add_variable(id, "defined")
                    if self._expect("VALUE", 3, token_index+3):
                        i = 4
                        value = self._expression(token_index+i)
                        while value["token_type"] != "string" or self._lexer.tokenized_code[token_index+i][0] != "ENDLINE":
                            variable_value = self._expression(token_index+i)
                            i += 1
                        return self._create_new_token("variable_string", id, variable_value)
        if self._accept("VARIABLE", token_index):
            id = self._lexer.tokenized_code[token_index][1]
            self._add_variable(id, "all")
            if self._expect("FUNC", 1, token_index+1):
                self._add_variable(id, "import")
                arguments = []
                arg = 1
                arg_num = 0
                while True:
                    arg = self._expression(token_index + 2 + arg_num)
                    if arg != False:
                        arguments.append(arg)
                        arg_num += 1
                    else:
                        break
                token_index += 2 + len(arguments)
                return self._create_new_token("function", id, arguments)
        return False
    
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
            return self._create_new_token("variable", variable)
        return False
    
    def _create_new_token(self, type, value="", children=[]):
        new_token = {"token_type": type, "token_value": value, "children": children}
        return new_token
        
    def _parse(self):
        while self.token_index < len(self._lexer.tokenized_code):
            statement = self._statement(self.token_index)
            if statement != False:
                self.parsed_code["body"].append(statement)
            self.token_index += 1
