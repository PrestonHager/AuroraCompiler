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
| WORD              | print                         | 1, 1      |
+-------------------+-------------------------------+-----------+
| FUNC              | >                             | 1, 6      |
+-------------------+-------------------------------+-----------+
| STRING_DEF        | "                             | 1, 7      |
+-------------------+-------------------------------+-----------+
| WORD              | Somewhere                     | 1, 8      |
+-------------------+-------------------------------+-----------+
| SPACE             |                               | 1, 16     |
+-------------------+-------------------------------+-----------+
| WORD              | over                          | 1, 17     |
+-------------------+-------------------------------+-----------+
| SPACE             |                               | 1, 21     |
+-------------------+-------------------------------+-----------+
| WORD              | the                           | 1  22     |
+-------------------+-------------------------------+-----------+
| SPACE             |                               | 1, 25     |
+-------------------+-------------------------------+-----------+
| WORD              | rainbow!                      | 1  26     |
+-------------------+-------------------------------+-----------+
| END_STRING_DEF    | "                             | 1, 34    |
+-------------------+-------------------------------+-----------+
| ENDLINE           | ;                             | 1, 35    |
+-------------------+-------------------------------+-----------+

Timeline?
~~~~~~~~~

-  **Day 1:** Create a list of token types and definitions. Then start
   on lexer code.
-  **Day 2:** Continue working on lexer code and complete it.
-  **Day 3:** Polish the lexer, fix any bugs.

.. _Parser page: http://auroracompiler.rtfd.io/en/latest/parser.html
.. _Synatax page.: http://auroracompiler.rtfd.io/en/latest/syntax.html
