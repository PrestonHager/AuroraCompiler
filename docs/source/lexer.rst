Lexer/Tokenizer
===============

What does this do?
~~~~~~~~~~~~~~~~~~

The lexer or tokenizer (hereby referred to as “the lexer”), will read the
given content — usually a file — character by character without
backtracking. The lexer detects spaces, separators, or other key
characters to *tokenize* the content. These tokens are in a array
(list), with the token type, the value, and the position(s). The parser
will take these tokens next. For more see the `Parser page`_, or
`Syntax page.`_

Input & Output
^^^^^^^^^^^^^^

The input is the actual code. This is in an ASCII or Unicode encoding,
basically plain text. The output is a list of tokens, which is usually
shown as a table in human-friendly formats. A token is yet another list,
or rather a tuple, containing the token name, token value, and position.
The following is an example of an input and output for the Lexer.

Input:

.. code::

    print>"Somewhere over the rainbow!";

Output:

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
