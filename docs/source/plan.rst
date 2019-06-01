Plan
====

What is “this” exactly?
~~~~~~~~~~~~~~~~~~~~~~~

The Aurora Compiler is just yet another compiler. It’s goal is to help
me (the author) practice and learn writing compilers. Eventually this
will lead to making a compiler in either C or Assembly for my OS,
`Startaste.`_

What technology is used?
~~~~~~~~~~~~~~~~~~~~~~~~

This compiler is written entirely in Python, and compiles to assembly.
GitHub is used for version control and releases,
and Read the Docs is used for documentation.

What are the features?
~~~~~~~~~~~~~~~~~~~~~~

The Aurora Compiler includes a Lexer, or Tokenizer, which creates an array
(list) of tokens for the parser. The next item is a parser, it will put
the tokens into a logical order for the generator. Next up, the
generator. This will create Assembly code based on what the parser outputs
and then the compiler can run an assembler such as NASM on the file to
assemble it to bytecode.

.. _Startaste.: https://github.com/PrestonHager/Startaste
