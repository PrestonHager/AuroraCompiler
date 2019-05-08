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
        nodes = []
        i = 0
        while i < len(self.lexer.lexed_code):
            node, increase = self._parse(self.lexer.lexed_code, i)
            if node != None:
                nodes.append(node)
            i += increase
        self.ast.add_children(*nodes)
        self._check(self.ast)
        print(self.ast)

    def _parse(self, tokens, index):
        node = None
        increase = 1
        if self._parse_check("COMMENT", tokens, index):
            increase += self._find_token(tokens[index+1:], "NEWLINE")
            comment_end = index + increase
            comment = ''.join([t.value for t in tokens[index+1:comment_end]])
            node = ASTNode("COMMENT").add_child(ASTValue(comment))
        if self._parse_check("FUNCTION", tokens, index):
            increase += self._find_token(tokens[index+1:], "ENDLINE")
            end_line = index + increase
            node = ASTNode("FUNCTION").add_child(ASTNode("ARGUMENTS").add_children(*[])).add_child(ASTValue("test", "NAME"))
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
        return True
