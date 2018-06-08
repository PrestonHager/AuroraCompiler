Subset 1
========

The first subset of the Aurora Language. The following will describe
what it includes, and what the end goal of the subset is. The first
subset is simply a way of measuring when part of the compiler is
finished. It includes all the functions that will be compilable within
the first subset. Future subsets will be describe as the language
developes further.

Features
~~~~~~~~

The first subset will include function calls. And one variable definition.

Any call to any function name can be called. The first one however, will
be the ``print`` statement.

Secondly variable definitions of strings will be possible. This means
that variables with the content of a string may be defined, and called
upon. For example if the variable ``String: hello = "Salutations to you!";``
may be defined and then later called with ``println>hello;``. This will
in turn print the line ``Salutations to you!`` with a newline at the end.

There will also be three predefined functions that may be called. The
first is the include function, syntax is as follows, ``include>[library];``.
For example if using, ``include>io;`` then any code that follows will
be able to use any I/O functions. I/O functions are also included in
this subset, they are ``print`` and ``println``. They do as described,
and more can be found on the `Syntax`_ page.

.. _Syntax: http://auroracompiler.rtfd.io/en/latest/syntax.html
