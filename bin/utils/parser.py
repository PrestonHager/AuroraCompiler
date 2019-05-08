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
        i = 0
        # loop over the lexed code and parse it.
        while i < len(self.lexer.lexed_code):
            # parse at position `i` in the lexed code
            node, increase = self._parse(self.lexer.lexed_code, i)
            if node != None:
                # if the node isn't None (meaning no parse could be done), we add it to the nodes list
                nodes.append(node)
            # and always increase the index of lexed code by at least 1, possibly more.
            i += increase
        # add all the nodes to the abstract syntax tree (AST)
        self.ast.add_children(*nodes)
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
            # increase the index until the end of the line, or the end of the function token (end of function either way).
            # choose the closest one to the current index aka smallest, but not 0
            endline = self._find_token(tokens[index+1:], "ENDLINE")
            func_end = self._find_token(tokens[index+1:], "FUNCTION_END")
            if endline == 0 or func_end == 0:
                increase += max(endline, func_end)+1
            else:
                increase += min(endline, func_end)+1
            arguments = []
            argument_tokens = tokens[index+1:index+increase]
            i = 0
            while i < len(argument_tokens):
                node, add = self._parse_arguments(argument_tokens, i)
                if node != None:
                    arguments.append(node)
                i += add
            name = tokens[index-1].value
            node = ASTNode("FUNCTION").add_child(ASTNode("ARGUMENTS").add_children(*arguments)).add_child(ASTValue(name, "NAME"))
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
        return (node, increase)

    def _find_token(self, tokens, token):
        index = 0
        for i in range(len(tokens)):
            if tokens[i].name == token:
                index = i
                break
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
