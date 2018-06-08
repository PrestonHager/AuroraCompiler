I/O Library
===========

The Input/Ouput library is used for simple input and output functions.
This is a builtin library included with the compiler and can be used
by any Aurora program.

The following are the functions of the library and a description of how to use them.

Print
~~~~~

Syntax
^^^^^^

``print>variable;``, ``print>"string";``, or ``print>number;``.

Usage
^^^^^

Print will write exactly that variable, string, or number, as a string, to the terminal.
Or more precisely the standard out file. However, be careful when using, because it will not
print a newline at the end like many programming languages do. Instead you must use the``println`` function to print something with a newline at the end.

Print - Line New
~~~~~~~~~~~~~~~~

Syntax
^^^^^^

``println>variable;``, ``println>"string";`, or ``println>number;``.

Usage
^^^^^

Much like Print, Print - Line New will print a variable, string, or number, as a string
to the standard out file. However, it will also print a newline at the end of it. This is
similar to the Python ``print`` function.

Input
~~~~~

Syntax
^^^^^^

``input>variable;``, ``input>"string";`, or ``input>number;``.

Usage
^^^^^

Input will print a variable, string, or number to the standard out file with ``println`` and
then ask for user input by reading a full line in the standard in file. That is it reads
user input until a newline or carriage return is pressed.
