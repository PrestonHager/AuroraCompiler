Lexer/Tokenizer
===============

What does this do?
~~~~~~~~~~~~~~~~~~

The lexer or tokenizer (hereby refered to as “the lexer”), will read the
given content — usually a file — character by character without
backtracking. The lexer detects spaces, seperators, or other key
characters to *tokenize* the content. These tokens are in a array
(list), with the token type, the value, and the position(s). The parser
will take these tokens next. For more see the `Parser page`_, or
`Synatax page.`_

Input & Output
^^^^^^^^^^^^^^

The input is the actual code. This is in an asii or unicode encoding,
basically plain text. The output is a list of tokens, which is usually
shown as a table in human-friendly formats. A token is yet another list,
or rather a tuple, containing the token name, token value, and position.
The following is an example of an input and output for the Lexer.

Input:

.. code::
    
    print>"Somewhere over the rainbow!";

Ouput:

+-------------------+-------------------------------+-----------+
| Token ID          | Token Value                   | Position  |
+===================+===============================+===========+
| ID                | print                         | 1, 1      |
+-------------------+-------------------------------+-----------+
| FUNC              | >                             | 6, 1      |
+-------------------+-------------------------------+-----------+
| STRING_DEF        | "                             | 7, 1      |
+-------------------+-------------------------------+-----------+
| ID                | Somewhere over the rainbow!   | 8, 1      |
+-------------------+-------------------------------+-----------+
| END_STRING_DEF    | "                             | 14, 1     |
+-------------------+-------------------------------+-----------+
| ENDLINE           | ;                             | 15, 1     |
+-------------------+-------------------------------+-----------+

Timeline?
~~~~~~~~~

-  **Day 1:** Create a list of token types and definitions. Then start
   on lexer code.
-  **Day 2:** Continue working on lexer code and complete it.
-  **Day 3:** Polish the lexer, fix any bugs.

.. _Parser page: http://auroracompiler.rtfd.io/en/latest/parser.html
.. _Synatax page.: http://auroracompiler.rtfd.io/en/latest/syntax.html
