I/O Library
===========

The Input/Output library, or IO for short, is used for simple input and output functions.
This is a built-in library included with the compiler and can be used by any Aurora program.

The following are the functions of the library and a description of how to use them.

IO In
~~~~~

Syntax
^^^^^^

``io_in>location;``.

Usage
^^^^^

Used to access the IO ports. The returned value is the value in the location of "location".

IO Out
~~~~~~

Syntax
^^^^^^

``io_out>location, value;``.

Usage
^^^^^

Also used to access the IO ports. The location, "location" will be passed
the value of "value".
