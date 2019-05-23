# ASTTools.py
# by Preston Hager
# for Aurora Compiler

class ASTBase:
    type = "NODE"

    def __init__(self, name="BASE", ntype="NODE", value=None, children=[]):
        type = ntype
        self.name = name
        self.value = value
        self.children = children

    def add_child(self, child):
        self.children.append(child)
        return self

    def add_children(self, *children):
        for child in children:
            self.children.append(child)
        return self

    def __repr__(self):
        if self.children != None:
            if self.value != None:
                return f"<{self.__class__.__name__}({len(self.children)}) {self.name}{{{self.value}}}: {self.children}>"
            else:
                return f"<{self.__class__.__name__}({len(self.children)}) {self.name}: {self.children}>"
        else:
            return f"<{self.__class__.__name__} {self.name}: `{self.value}`>"

    def __str__(self):
        return self.__repr__()

class ASTNode(ASTBase):
    type = "NODE"

    def __init__(self, name):
        super().__init__(name, ntype="NODE", value=None, children=[])

class ASTValue(ASTBase):
    type = "VALUE"

    def __init__(self, value, name=None):
        super().__init__(name, ntype="VALUE", value=value, children=None)

__all__ = ["ASTBase", "ASTNode", "ASTValue"]
