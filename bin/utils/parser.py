# parser.py
# by Preston Hager
# for Aurora Compiler

# Probably also important imports.
import os
import shutil
from utils.ASTTools import *
from utils.errors import ParserError
from utils.constants import OPERATIONS

class Parser:
    def __init__(self, lexer, extra):
        """
        Creates a new Parser instance

        Parameters
        ----------
        lexer : Lexer
            Lexer to link to the parser

        Returns
        -------
        Parser
            New Parser instance with previous parameters.
        """
        self.lexer = lexer
        self.extra = extra
        self.dependencies = []
        self.ast = ASTBase(children=[])

    def parse(self):
        """
        Parses the tokenized code from the lexer.
        """
        # define a few helpful variables. nodes holds each "line" of code in order, i is just the index of the lexed code.
        nodes = []
        definition_nodes = []
        i = 0
        # loop over the lexed code and parse it.
        while i < len(self.lexer.lexed_code):
            # parse at position `i` in the lexed code
            node, increase = self._parse(self.lexer.lexed_code, i)
            if node != None:
                # if the node isn't None (meaning no parse could be done), we add it to the nodes list
                if node.name == "FUNCTION_DEFINTION":
                    definition_nodes.append(node)
                else:
                    nodes.append(node)
            # and always increase the index of lexed code by at least 1, possibly more.
            i += increase
        # add all the nodes to the abstract syntax tree (AST)
        self.ast.add_children(*nodes+definition_nodes)
        # check the ast for any parser errors, i.e. undefined variables
        self._check(self.ast)
        # print(self.ast) # debug

    def _parse(self, tokens, index):
        # the return variables are set to the default.
        node = None
        increase = 1
        # check for a comment token ("//")
        if self._parse_check("COMMENT", tokens, index):
            # increase the index until the end of the line (end of comment)
            increase += self._find_token(tokens[index+1:], "NEWLINE")
            comment_end = index + increase
            comment = ''.join([t.value for t in tokens[index+1:comment_end]])
            node = ASTNode("COMMENT").add_child(ASTValue(comment))
        elif self._parse_check("FUNCTION", tokens, index):
            # find the end of the function and increase the index to at least there.
            increase += self._find_function_end(tokens[index+1:])
            # get the name of the function because a for loop is sort of a function.
            name = tokens[index-1].value
            if name == "for":
                # a for loop has three arguments.
                # initialization statement, test statement/condition, loop statement (executed at the end of each loop).
                # TODO: add for loop parsing
                for_nodes = []
                for_tokens = tokens[index+1:index+increase]
                i = 0
                while i < len(for_tokens):
                    node, add = self._parse_arguments(for_tokens, i)
                    if node != None:
                        for_nodes.append(node)
                    i += add
                # if the list of arguments is less than three then it's not a valid for loop.
                if len(for_nodes) < 3:
                    raise ParserError(f"Invalid for loop, perhaps you added a `;` instead of a `,`. At {tokens[index].position[0]}, {tokens[index].position[1]}")
                # test to see if the next token is a `then`, if it is then we parse the code until an `end`, otherwise it's just one line that we parse for the for loop.
                if self._find_token(tokens[index+increase:index+increase+2], "THEN"):
                    # parse until the end token
                    parse_until = self._find_token(tokens[index+increase:], "END")+1
                else:
                    # parse just until the next endline
                    parse_until = self._find_token(tokens[index+increase:], "ENDLINE")+1
                # parse all the code, actually. This is very similar to parsing for arguments.
                code_nodes = []
                code_tokens = tokens[index+increase:index+increase+parse_until]
                i = 0
                while i < len(code_tokens):
                    node, add = self._parse(code_tokens, i)
                    if node != None:
                        code_nodes.append(node)
                    i += add
                # TODO: add node for for loop.
                increase += parse_until
                node = ASTNode("FOR").add_child(
                        ASTNode("INITIALIZATION").add_child(for_nodes[0])).add_child(
                        ASTNode("CONDITION").add_child(for_nodes[1])).add_child(
                        ASTNode("LOOP").add_child(for_nodes[2])).add_child(
                        ASTNode("CODE").add_children(*code_nodes))
            # if the function isn't a function then we do normal function stuff.
            else:
                # find the arguments of the function.
                # you may notice this code is very similar to that in `self.parse`.
                arguments = []
                argument_tokens = tokens[index+1:index+increase]
                i = 0
                while i < len(argument_tokens):
                    node, add = self._parse_arguments(argument_tokens, i)
                    if node != None:
                        arguments.append(node)
                    i += add
                # if the funciton is an include function we will parse it as such.
                if name == "include":
                    # the file to include is "homemade" if it is a string, and a standard library if it's just a word.
                    if arguments[0].name == "STRING":
                        file = arguments[0].value + ".asm"
                        self.dependencies.append([arguments[0].value + ".aurora", file])
                    elif self.extra["freestanding"]:
                        if not os.path.exists(os.path.join("aurora", "libraries")):
                            os.makedirs(os.path.join("aurora", "libraries"))
                        shutil.copy(os.path.join(self.lexer.bin_dir, "libraries", "_aurora_" + arguments[0].value + ".asm"), os.path.join("aurora", "libraries", "_aurora_" + arguments[0].value + ".asm"))
                        file = os.path.join("aurora", "libraries", "_aurora_" + arguments[0].value + ".asm")
                    else:
                        file = os.path.join(self.lexer.bin_dir, "libraries", "_aurora_" + arguments[0].value + ".asm")
                    node = ASTNode("INCLUDE").add_child(
                            ASTValue(file, "FILE")).add_child(
                            ASTValue(name, "NAME"))
                # if we get here the function is pretty normal, just a normal function call and we parse it as such.
                else:
                    node = ASTNode("FUNCTION").add_child(
                            ASTNode("ARGUMENTS").add_children(*arguments)).add_child(
                            ASTValue(name, "NAME"))
        # check for a function definition.
        elif self._parse_check("FUNCTION_DEFINTION", tokens, index):
            ## TODO: comment this code so someone, or even I, can understand it.
            endline = self._find_token(tokens[index+1:], "ENDLINE")
            parameters = []
            parameter_tokens = tokens[index+4:index+endline]
            i = 0
            while i < len(parameter_tokens):
                node, add = self._parse_parameters(parameter_tokens, i)
                if node != None:
                    parameters.append(node)
                i += add
            name = tokens[index+2].value
            # the code within the function is added to this node and parsed now.
            nodes = []
            i = endline
            end_found = False
            while not end_found:
                node, add = self._parse(tokens[index:], i)
                if node != None:
                    if node.name == "END":
                        end_found = True
                    else:
                        nodes.append(node)
                i += add
            increase += i
            node = ASTNode("FUNCTION_DEFINTION").add_child(
                    ASTNode("PARAMETERS").add_children(*parameters)).add_child(
                    ASTNode("CODE").add_children(*nodes)).add_child(
                    ASTValue(name, "NAME"))
        # check for a variable definition.
        elif self._parse_check("VARIABLE", tokens, index):
            endline = self._find_token(tokens[index+1:], "ENDLINE")
            comma = self._find_token(tokens[index+1:], "COMMA")
            if endline == 0 or comma == 0:
                increase += max(endline, comma)
            else:
                increase += min(endline, comma)
            name_index = self._find_token(tokens[index+1:], "WORD")
            name = tokens[index+1+name_index].value
            value = self._parse_value(tokens[index+3+name_index:index+increase+1])[0]
            if value == None:
                value = ASTValue("0", "NUMBER")
            if tokens[index-1].name == "NUMBER_KEYWORD":
                type = "NUMBER"
            elif tokens[index-1].name == "STRING_KEYWORD":
                type = "STRING"
            else:
                raise ParserError(f"The variable type `{tokens[index-1].value}` is not yet supported. At {tokens[index].position[0]}, {tokens[index].position[1]}")
            node = ASTNode("VARIABLE_DEFINITION").add_child(
                    ASTNode("VALUE").add_child(value)).add_child(
                    ASTValue(name, "NAME")).add_child(
                    ASTValue(type, "TYPE"))
        # check for a variable assignment (i.e. EQUALS, PLUS_EQUALS, and MINUS_EQUALS).
        elif self._parse_check("EQUALS", tokens, index):
            node, increase = self._variable_assignment(tokens, index, increase)
        elif self._parse_check("PLUS_EQUALS", tokens, index):
            node, increase = self._variable_assignment(tokens, index, increase, "PLUS", False, False)
        elif self._parse_check("PLUS_EQUALS_ONE", tokens, index):
            node, increase = self._variable_assignment(tokens, index, increase, "PLUS", False, True)
        elif self._parse_check("MINUS_EQUALS", tokens, index):
            node, increase = self._variable_assignment(tokens, index, increase, "MINUS", False, False)
        elif self._parse_check("MINUS_EQUALS_ONE", tokens, index):
            node, increase = self._variable_assignment(tokens, index, increase, "MINUS", False, True)
        # TODO: add the plus_equals, minus_equals, minus_equals_one tokens here
        elif self._parse_check("END", tokens, index):
            node = ASTNode("END")
        return (node, increase)

    def _variable_assignment(self, tokens, index, increase, operation=None, is_equals=True, is_one=False):
        pointer = False
        endline = self._find_token(tokens[index+1:], "ENDLINE")+1
        increase = endline
        if self._find_token(tokens[index-3:index], "POINTER_END"):
            name_index = self._find_token(tokens[index-5:index], "WORD")
            name = tokens[index-5+name_index].value
            pointer = True
        else:
            name_index = self._find_token(tokens[index-2:index], "WORD")
            name = tokens[index-2+name_index].value
        # before parsing the value we must check for the `byte`, `word`, and `dword` keywords.
        # if one of these is found then that size must be maintained when assignning the value to the variable.
        # to do this we add an ASTNode in the `node` which says "SIZE" is `byte`, `word`, or `dword`.
        size = ASTValue("DOUBLE_WORD", "SIZE")
        for s in ["BYTE", "WORD", "DOUBLE_WORD"]:
            size_index = self._find_token(tokens[index+1:], s+"_KEYWORD")
            if size_index > 0:
                size = ASTValue(s, "SIZE")
        if not is_equals and is_one:
            value = ASTNode("POSTFIX").add_children(
                    ASTValue(name, "VARIABLE"), ASTValue("1", "NUMBER"), ASTValue(None, operation))
        elif not is_equals and not is_one:
            value = ASTNode("POSTFIX").add_child(
                    ASTValue(name, "VARIABLE")).add_children(
                    *self._parse_value(tokens[index+1+size_index:index+endline+1])[0].children).add_child(
                    ASTValue(None, operation))
        else:
            value = self._parse_value(tokens[index+1+size_index:index+endline+1])[0]
        node = ASTNode("VARIABLE_ASSIGNMENT").add_child(
                size).add_child(
                ASTNode("VALUE").add_child(value)).add_child(
                ASTNode("VARIABLE").add_child(
                    ASTValue(name, "NAME")).add_child(
                    ASTValue(pointer, "POINTER"))
                )
        return (node, increase)

    def _parse_value(self, tokens, index=0):
        # We parse the value by creating a "postfix" for the original "infix".
        operation_stack = []
        postfix = ASTNode("POSTFIX")
        while index < len(tokens) and not (tokens[index].name == "GROUP_END" or tokens[index].name == "COMMA" or tokens[index].name == "ENDLINE"):
            token = tokens[index]
            index += 1
            if token.name in OPERATIONS:
                if len(operation_stack) > 0 and OPERATIONS[token.name] < OPERATIONS[operation_stack[-1]]:
                    while len(operation_stack) > 0:
                        postfix.add_child(ASTValue(None, operation_stack.pop()))
                operation_stack.append(token.name)
            elif token.name == "FUNCTION":
                postfix.children.pop().value
                node, increase = self._parse(tokens, index-1)
                postfix.add_child(node)
                index += increase
            elif token.name == "GROUP_START":
                group_postfix, index = self._parse_value(tokens, index)
                postfix.add_children(*group_postfix.children)
            elif token.name == "STRING_DEFINITION":
                node, increase = self._parse_arguments(tokens, index-1)
                postfix.add_child(node)
                index += increase
            elif token.name == "NUMBER":
                postfix.add_child(ASTValue(token.value, "NUMBER"))
            elif token.name == "WORD":
                postfix.add_child(ASTValue(token.value, "VARIABLE"))
        while len(operation_stack) > 0:
            postfix.add_child(ASTValue(None, operation_stack.pop()))
        return (postfix, index)

    def _parse_group(self, tokens, index, postfix):
        operation_stack = []
        while tokens[index].name != "GROUP_END":
            token = tokens[index]
            if token.name in OPERATIONS:
                if len(operation_stack) > 0 and OPERATIONS[token.name] < OPERATIONS[operation_stack[-1]]:
                    while len(operation_stack) > 0:
                        postfix.add_child(ASTValue(None, operation_stack.pop()))
                operation_stack.append(token.name)
            elif token.name == "GROUP_START":
                self._parse_group(tokens, index+1, postfix)
            elif token.name == "NUMBER":
                postfix.add_child(ASTValue(token.value, "NUMBER"))
            elif token.name == "WORD":
                postfix.add_child(ASTValue(token.value, "VARIABLE"))
            index += 1
        while len(operation_stack) > 0:
            postfix.add_child(ASTValue(None, operation_stack.pop()))

    def _find_number_variable(self, tokens, index):
        i = 1
        value1 = tokens[index-1]
        value2 = tokens[index+1]
        while (value1.name != "NUMBER" or value1.name != "WORD") and (value2.name != "NUMBER" or value1.name != "WORD"):
            i += 1
            if value1.name != "NUMBER" and value1.name != "WORD":
                value1 = tokens[index-i]
            if value2.name != "NUMBER" and value2.name != "WORD":
                value2 = tokens[index+i]
        if value1.name == "NUMBER":
            value1 = ASTValue(value1.value, "NUMBER")
        else:
            value1 = ASTValue(value1.value, "VARIABLE")
        if value2.name == "NUMBER":
            value2 = ASTValue(value2.value, "NUMBER")
        else:
            value2 = ASTValue(value2.value, "VARIABLE")
        return (value1, value2)

    def _parse_parameters(self, tokens, index):
        node, increase = self._parse(tokens, index)
        if node != None:
            return (node, increase)
        return (node, increase)

    def _parse_arguments(self, tokens, index):
        # first parse the normal tokens
        node, increase = self._parse(tokens, index)
        # the _parse function will always look at the `;` token for the increase variable.
        # we must look for a comma first and then go with the endline token.
        comma = self._find_token(tokens[index:index+increase], "COMMA")
        if comma != 0:
            increase = comma
        # if the values aren't the default then return otherwise just continue.
        if node != None:
            return (node, increase)
        if self._parse_check("STRING_DEFINITION", tokens, index):
            # increase the index until the end of the string.
            string_end = self._find_token(tokens[index+1:], "STRING_DEFINITION")
            increase += string_end+1
            string = ""
            for token in tokens[index+1:index+string_end+1]:
                string += token.value
            node = ASTValue(string, "STRING")
        # try to find a test token, these are prefixed with ? and are comparisons.
        # the reason we include the token before index, is because if the test returns 0, the parser thinks it's false. So by adding the token the test returns 1, which we subtract 1 to get index.
        elif self._find_test_tokens(tokens[index-1:index+1]):
            # find the end of the comparison, either a comma, or an endline.
            increase = min([i for i in [self._find_token(tokens[index+2:], "COMMA"), self._find_token(tokens[index+2:], "ENDLINE")] if i != 0])+3
            # then find the last argument, either a comma or a function call.
            last_argument = index
            while last_argument > 0:
                if tokens[last_argument].name == "COMMA" or tokens[last_argument].name == "FUNCTION":
                    last_argument += 1
                    break
                last_argument -= 1
            # then parse the values on either side of the comparison.
            parsed_value1 = self._parse_value(tokens[last_argument:index])
            parsed_value2 = self._parse_value(tokens[index+1:index+increase-1])
            value1 = parsed_value1[0]
            value2 = parsed_value2[0]
            # and finally, create a node from these values and comparison token.
            node = ASTNode("COMPARISON").add_child(
                    ASTValue(tokens[index].name, "TEST")).add_child(
                    ASTNode("VALUE_1").add_child(value1)).add_child(
                    ASTNode("VALUE_2").add_child(value2))
        elif self._parse_check("WORD", tokens, index):
            # test for a word so we can add it as a variable, as long as it's not a function call, part of an assingment, or part of a comparison.
            if self._find_token(tokens[index:index+1], "FUNCTION") == 0 and self._find_test_tokens(tokens[index:index+3]) == 0 and self._find_variable_assignment_tokens(tokens[index:index+2]) == 0:
                node = ASTValue(tokens[index].value, "VARIABLE")
        elif self._parse_check("NUMBER", tokens, index):
            # add any numbers as an ASTValue of NUMBER.
            node = ASTValue(tokens[index].value, "NUMBER")
        return (node, increase)

    def _find_token(self, tokens, token):
        # helpful internal funciton for finding tokens in a given range.
        index = 0
        for i in range(len(tokens)):
            if tokens[i].name == token:
                index = i
                break
        return index

    def _find_test_tokens(self, tokens):
        # helpful internal funciton for finding comparison (test) tokens.
        equals_test = self._find_token(tokens, "EQUALS_TEST")
        not_equals_test = self._find_token(tokens, "NOT_EQUAL_TEST")
        less_than_test = self._find_token(tokens, "LESS_THAN_TEST")
        great_than_test = self._find_token(tokens, "GREATER_THAN_TEST")
        less_than_equal_test = self._find_token(tokens, "LESS_THAN_EQUAL_TEST")
        greater_than_equal_test = self._find_token(tokens, "GREATER_THAN_EQUAL_TEST")
        non_zero = [i for i in [equals_test, not_equals_test, less_than_test, great_than_test, less_than_test, greater_than_equal_test] if i != 0]
        return min(non_zero) if len(non_zero) > 0 else 0

    def _find_variable_assignment_tokens(self, tokens):
        # helpful interal function for finding assingment tokens.
        equals = self._find_token(tokens, "EQUALS")
        plus_equals = self._find_token(tokens, "PLUS_EQUALS")
        plus_equals_one = self._find_token(tokens, "PLUS_EQUALS_ONE")
        minus_equals = self._find_token(tokens, "MINUS_EQUALS")
        minus_equals_one = self._find_token(tokens, "MINUS_EQUALS_ONE")
        non_zero = [i for i in [equals, plus_equals, plus_equals_one, minus_equals, minus_equals_one] if i != 0]
        return min(non_zero) if len(non_zero) > 0 else 0

    def _find_function_end(self, tokens):
        # increase the index until the end of the line, or the end of the function token (end of function either way).
        bracket = 1
        index = 0
        while bracket != 0:
            if tokens[index].name == "FUNCTION":
                bracket += 1
            elif tokens[index].name == "FUNCTION_END":
                bracket -= 1
            elif tokens[index].name == "ENDLINE":
                bracket = 0
            index += 1
        return index

    def _check(self, ast):
        pass

    def _parse_check(self, type, tokens, i):
        # helpful interal function to check that a token has the required surrounding tokens.
        # TODO: update for all other tokens.
        if tokens[i].name != type:
            return False
        if type == "FUNCTION":
            if i == 0:
                raise ParserError(f"Expected a function name before function call. At {tokens[i].position[0]}, {tokens[i].position[1]}")
            if tokens[i-1].name != "WORD":
                raise ParserError(f"Expected a function name before function call. At {tokens[i-1].position[0]}, {tokens[i-1].position[1]}")
            if self._find_token(tokens[i+1:], "ENDLINE") == 0 and self._find_token(tokens[i+1:], "FUNCTION_END") == 0:
                raise ParserError(f"Function must end with either `<` or `;`. At {tokens[i].position[0]}, {tokens[i].position[1]}")
        if type == "STRING_DEFINITION":
            if self._find_token(tokens[i+1:], "STRING_DEFINITION") == 0:
                raise ParserError(f"String doesn't end. At {tokens[i].position[0]}, {tokens[i].position[1]}")
        return True
