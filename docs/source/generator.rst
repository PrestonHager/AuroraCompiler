Generator
=========

What does this do?
~~~~~~~~~~~~~~~~~~

The Generator is the next, and the near last step of the compiler.
It creates Assembly code based on the AST that the parser generates.
This is quite hard because you're taking abstract ideas and concepts
and putting them into assembly code.

Input & Output
^^^^^^^^^^^^^

The input is an Abstract Syntax Tree (AST) from the Parser.
The output is assembly code that can be assembled using something like NASM.

Input:

.. code::

    <ASTNode(l) FUNCTION: [
      <ASTValue NAME: "print">,
      <ASTNode(1) ARGUMENTS: [
        <ASTValue STRING: "Somewhere over the rainbow!">
      ]>
    ]>

Output:

.. code::

    mov [_aurora_arg_buffer+4], DWORD _aurora_[hex_string]_string_0
    call print

    _aurora_arg_buffer times 32 dq 0
    _aurora_[hex_string]_string_0 db "Somewhere over the rainbow!", 0
