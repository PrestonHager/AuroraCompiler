# aurora_lexer.py

class AuroraLexer:
    def __init__(self, code):
        self.tokenized_code = []
        self.lex(code)

    def lex(self, code):
        current_id = ""
        for char in code:
            if char in self.operations:
                self.tokenized_code
