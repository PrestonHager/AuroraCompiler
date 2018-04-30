# Lexer/Tokenizer

### What does this do?

The lexer or tokenizer (hereby refered to as "the lexer"), will read the given content
— usually a file —
character by character without backtracking.
The lexer detects spaces, seperators, or other key characters to *tokenize* the content.
These tokens are in a array (list), with the token type, the value, and the position(s).
The parser will take these tokens next.
For more see the [Parser page](http://auroracompiler.rtfd.io/en/latest/parser), or [Synatax page.](https://auroracompiler.rtfd.io/en/latest/syntax)

--------
### Timeline?

* **Day 1:** Create a list of token types and definitions. Then start on lexer code.
* **Day 2:** Continue working on lexer code and complete it.
* **Day 3:** Polish the lexer, fix any bugs.
