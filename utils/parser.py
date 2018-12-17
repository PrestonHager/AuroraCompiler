# parser.py
# by Preston Hager
# for Aurora Compiler

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.ast = ASTNode("TOP_LEVEL")

    def parse(self):
        pass

class ASTNode:
    def __init__(self, type):
        self.type = type
        self.children = []
        self.children_amount = 0

    def __str__(self):
        return f"<ASTNode `{self.type}`: {self.children_amount} children.>"

    def add_child(self, child):
        self.children.append(child)
        self.children_amount += 1

class ASTValue:
    def __init__(self, value):
        self.value = value

    def __str(self):
        return f"<ASTValue `{self.value}`>"
