# parser.py
# by Preston Hager
# for Aurora Compiler

from utils.ASTTools import *
from utils.errors import ParserError

class Parser:
    def __init__(self, lexer):
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
        self.ast = ASTBase()

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
        print(self.ast) # debug

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
                # test to see if the next token is a `then`, if it is then we parse the code until an `end`, otherwise it's just one line that we parse for the for loop.
                if self._find_token(tokens[index+increase:index+increase+2], "THEN"):
                    # parse until the end token
                    increase += self._find_token(tokens[index+increase:], "END")+1
                    parse_until = "END"
                else:
                    # parse just until the next endline
                    increase += self._find_token(tokens[index+increase:], "ENDLINE")
                    parse_until = "ENDLINE"
                # TODO: add node for for loop.
                node = ASTNode("FOR").add_child(
                        ASTNode("INITIALIZATION").add_child(for_nodes[0])).add_child(
                        ASTNode("CONDITION").add_child(for_nodes[1])).add_child(
                        ASTNode("LOOP").add_child(for_nodes[2])).add_child(
                        ASTNode("CODE"))
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
                    else:
                        file = "_aurora_" + arguments[0].value + ".asm"
                    node = ASTNode("INCLUDE").add_child(
                            ASTValue(file, "FILE")).add_child(
                            ASTValue(name, "NAME"))
                # if we get here the function is pretty normal, just a normal function call and we parse it as such.
                else:
                    node = ASTNode("FUNCTION").add_child(
                            ASTNode("ARGUMENTS").add_children(*arguments)).add_child(
                            ASTValue(name, "NAME"))
        elif self._parse_check("FUNCTION_DEFINTION", tokens, index):
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
        elif self._parse_check("VARIABLE", tokens, index):
            endline = self._find_token(tokens[index+1:], "ENDLINE")
            comma = self._find_token(tokens[index+1:], "COMMA")
            if endline == 0 or comma == 0:
                increase += max(endline, comma)
            else:
                increase += min(endline, comma)
            name_index = self._find_token(tokens[index+1:], "WORD")
            name = tokens[index+1+name_index].value
            value = self._parse_value(tokens[index+2+name_index:index+increase])
            if value == None:
                value = ASTValue("0", "VALUE")
            if tokens[index-1].name == "NUMBER_KEYWORD":
                type = "NUMBER"
            elif tokens[index-1].name == "STRING_KEYWORD":
                type = "STRING"
            else:
                raise ParserError(f"The variable type `{tokens[index-1].value}` is not yet supported. At {tokens[index].position[0]}, {tokens[index].position[1]}")
            node = ASTNode("VARIABLE_DEFINITION").add_child(
                    value).add_child(
                    ASTValue(name, "NAME")).add_child(
                    ASTValue(type, "TYPE"))
        elif self._parse_check("END", tokens, index):
            node = ASTNode("END")
        return (node, increase)

    def _parse_value(self, tokens):
        print(tokens)
        node = None
        return node

    def _parse_parameters(self, tokens, index):
        node, increase = self._parse(tokens, index)
        if node != None:
            return (node, increase)
        return (node, increase)

    def _parse_arguments(self, tokens, index):
        # first parse the normal tokens
        node, increase = self._parse(tokens, index)
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
        elif self._parse_check("WORD", tokens, index):
            if self._find_token(tokens[index+1:index+3], "FUNCTION") == 0 and self._find_token(tokens[index+1:index+3], "EQUALS") == 0:
                node = ASTValue(tokens[index].value, "VARIABLE")
        elif self._parse_check("NUMBER", tokens, index):
            node = ASTValue(tokens[index].value, "NUMBER")
        return (node, increase)

    def _find_token(self, tokens, token):
        index = 0
        for i in range(len(tokens)):
            if tokens[i].name == token:
                index = i
                break
        return index

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
