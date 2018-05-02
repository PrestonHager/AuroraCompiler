# aurora_parser.py

from aurora_lexer import AuroraLexer

class AuroraParser:
    def __init__(self, code):
        self._lexer = AuroraLexer(code)
        self._parse(self._lexer.tokenized_code)

    def _parse(self, tokens):
        pass
