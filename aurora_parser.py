# aurora_parser.py

from aurora_lexer import AuroraLexer

class AuroraParser:
    def __init__(self, code):
        self._lexer = AuroraLexer(code)
        self.parsed_code = {"body": [], "initialized": []}
        self._parse(self._lexer.tokenized_code)

    def _create_new_token(self, type, value="", children=[]):
        new_token = {"token_type": type, "token_value": value, "children": children}
        return new_token
        
    def _parse(self, tokens):
        pass
