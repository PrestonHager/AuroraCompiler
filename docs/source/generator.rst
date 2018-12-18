Generator
=========

What does this do?
~~~~~~~~~~~~~~~~~~

The Generator is the next, and last step of the compiler. It creates
Python code based on the AST that the parser generates. This is probably
one of the most simple steps and won’t require as much work to
implement.

Input & Ouput
^^^^^^^^^^^^^

The input is an Abstract Syntax Tree (AST) from the Parser. This will
output Python code to be executed. The following is an example.

Input:

.. code::

TOP_LEVEL = [
  FUNCTION = [
    ARGUMENTS = "Somewhere over the rainbow!"
  ]
]

Output:

.. code::

    mov si, _VAR_0
    push si
    call _aurora_print

    _VAR_0 db "Somewhere over the rainbow!", 0

Timeline?
~~~~~~~~~

-  **Day 1:** From the example ASTs created when developing the parser,
   create generated code.
-  **Day 2:** Write the pseudo for the generator, and then implement it
   in Python.
-  **Day 3:** Finish up Python code, and polish.
