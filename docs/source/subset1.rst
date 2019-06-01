Subset 1
========

The first subset of the Aurora Language. The following will describe
what it includes, and what the end goal of the subset is. The first
subset is simply a way of measuring when part of the compiler is
finished. It includes all the functions that will be compile-abled within
the first subset. Future subsets will be describe as the language
develops further.

Features
~~~~~~~~

The first subset will include function calls. Includes, A.K.A. imports.
And variable definitions for numbers and strings.

Any call to any function name can be called. This is really the base of
Aurora. Just specify the function name, use the ``>`` character, and
follow it with any arguments passed to the function. A function is closed
by either the ``<`` or ``;`` tokens. For example the following will call
a function called ``greet`` with an argument of ``"Aurora"``:
``greet>"Aurora";``. This does the same: ``greet>"Aurora"<;``.

Thirdly variable definitions of strings will be possible. This means
that variables with the content of a string may be defined, and called
upon. For example if the variable ``String: hello = "Salutations to you!";``
may be defined and then later called with ``println>hello;``. This will
in turn print the line ``Salutations to you!`` with a newline at the end.

Number variables are another variable that can be defined. This can be
done by specifying the ``Number`` variable. For example, ``Number: age = 15;``
will define a variable named ``age`` with a value of ``15``.

More on specific syntaxes can by found on the `Syntax`_ page.

.. _Syntax: http://auroracompiler.rtfd.io/en/latest/syntax.html
