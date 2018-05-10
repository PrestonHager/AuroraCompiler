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

This compiler is writen entirely in Python (because the client requested
it), and will compiler to Python code as well. GitHub is used for
version control and releases, and Read the Docs is used for
documentation.

What are the features?
~~~~~~~~~~~~~~~~~~~~~~

The Aurora Compiler includes a Lexer or Tokenizer which creates an array
(list) of tokens for the parser. The next item is a parser, it will put
the tokens into a logical order for the generator. Next up, the
generator. This will create Python code based on what the parser outputs
and will then be executable by a Python compiler.

Timeline?
~~~~~~~~~

-  **Week 0:** The plan.
-  **Week 1:** Define the language terminology and make an example file.
-  **Week 2:** Create the lexer/tokenizer.

   -  **Day 1:** Create a list of token types and definitions. Then
      start on lexer code.
   -  **Day 2:** Continue working on lexer code and complete it.
   -  **Day 3:** Polish the lexer, fix any bugs.

-  **Week 3-4:** Create the parser.

   -  **Day 1:** Create 1-2 example ASTs and companion code. Then write
      psuedo code for how it might execute.
   -  **Day 2:** Finish up the psuedo code. Then start on writing actual
      Python code.
   -  **Day 3:** Complete actual Python code, and then polish and squash
      those bugs!

-  **Week 5:** Create the generator.

   -  **Day 1:** From the example ASTs created when developing the
      parser, create generated code.
   -  **Day 2:** Write the pseudo for the generator, and then implement
      it in Python.
   -  **Day 3:** Finish up Python code, and polish.

-  **Week 6:** Debug week. Test as much as possible and find all the
   bugs and fix them.

.. _Startaste.: https://github.com/PrestonHager/Startaste