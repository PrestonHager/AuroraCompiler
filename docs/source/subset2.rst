Subset 2
========

The second subset of the Aurora Language. The following will describe
what it includes, and what the end goal of the subset is. Much like
the first subset, the second is a way of measuring what has been completed.

Features
~~~~~~~~

The second subset will include function definitions, number variable definitions,
and math operations.

A function may be defined by the programmer, to take in arguments and return a value.
More on how to define a function in the `Syntax`_ page.

Secondly variable definitions of number will be possible. This means
that variables with the content of a number may be defined, and called
upon. For example if the variable ``Number: age = 15;``, then it may be defined
and then later called with ``println(age);`` or any other number variable parameter.
This will in turn print the line ``15`` with a newline at the end.

Math can also be done. There are two ways of doing this, either with the Math library,
or with inline operations. To use the Math library, include it with ``include>math;``,
and call any function such as ``add>6, 2;``, which will return ``8``. The second way is
inline math operations, to do this requires no includes. Using ``+``, ``-``, ``*``, or ``/``count as inline math operations. So the code, ``6 + 2;`` also returns ``8``.

.. _Syntax: http://auroracompiler.rtfd.io/en/latest/syntax.html
