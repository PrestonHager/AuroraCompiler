String Library
==============

The String library is used for string manipulation. This is a built-in library
included with the compiler and can be used by any Aurora program.

The following are the functions of the library and a description of how to use them.

ASCII
~~~~~

Syntax
^^^^^^

``ascii>char;``.

Usage
^^^^^

Takes a ``String`` and returns the numerical ASCII value of the first character of the string.

Length
~~~~~~

Syntax
^^^^^^

``len>string;``.

Usage
^^^^^

Returns the length of the passed in string. To do this, the string must be
null-terminated which automatically happens when defining strings in Aurora.
