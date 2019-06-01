Subset 2
========

The second subset of the Aurora Language. The following will describe
what it includes, and what the end goal of the subset is. Much like
the first subset, the second is a way of measuring what has been completed.

Features
~~~~~~~~

The second subset will include function definitions, math operations, and
variable assignment.

A function may be defined by the programmer, to take in arguments and return a value.
When these arguments are defined by variable in the function they are called parameters.
More on how to define a function in the `Syntax`_ page.

Math is an extremely important aspect of programming. Now you can add,
subtract, multiply, and divide numbers. For example to define a
number variable with the product of 3 and 5 it would be ``Number:
age = 3 * 5;``. This method also works with variables. For example:
``Number: old = age * 4;`` would assign the value of 4 times ``age`` to ``old``.

Variable assignment means you don't have to redefine a variable each time you
want to assign a new value. So if we want to multiply ``age`` by 4
without reassigning it to ``old``, but keeping it in ``age`` we can write:
``age = age * 4;``. When adding or subtracting, you can do it without referencing
the variable twice by either the ``+=`` or ``-=`` operations. This cannot
be done with multiplication nor division. Additionally, the ``++`` and ``--``
operations will add and subtract 1 respectively.

More on specific syntaxes can by found on the `Syntax`_ page.

.. _Syntax: http://auroracompiler.rtfd.io/en/latest/syntax.html
