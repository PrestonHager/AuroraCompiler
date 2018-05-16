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

    {"body": [
        {
        "token_type": "function",
        "token_value": "print",
        "children": [
            {
                "token_type": "string",
                "token_value": "Hello!",
                "children": []
            }]
        }
    ]}

Output:

.. code::

    print("Somewhere over the rainbow!")

Timeline?
~~~~~~~~~

-  **Day 1:** From the example ASTs created when developing the parser,
   create generated code.
-  **Day 2:** Write the pseudo for the generator, and then implement it
   in Python.
-  **Day 3:** Finish up Python code, and polish.