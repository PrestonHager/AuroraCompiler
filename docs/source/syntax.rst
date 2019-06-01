Syntax
======

Definitions
~~~~~~~~~~~

The basis of all programming languages is definitions and math. To
define a variable in Aurora is simple. You must know the *type*, the
*name*, and a *value*. Definition is then as follows.

.. code::

    [Type]: [Name] = [Value]

There are many types, and one can also create their own variable type.
Names consist of standard ASCII characters, underscores, and digits; a
name must also not start with a digit (number). A value is constricted to
that variable’s type. For example if a variable’s type is ``Number``
then it must be an integer or float (a number). If the type is
``String`` then the value must be an array of characters defined by
``"[Value]"``. Notice the double quotation marks on either side of the
value.

A pointer can be "defined" by using square brackets (``[`` and ``]``).
So ``[video_memory] = byte ascii>"L";`` will assign the value of ``byte
ascii>"L"`` to the memory at the location of ``video_memory``. ``video_memory``
is most likely around ``0x8b000`` and will manipulate the screen somehow.

A list of types with their expected values can be found on the `Types`_
page.

Variable Manipulation
~~~~~~~~~~~~~~~~~~~~~

Variables can be manipulated by the ``=`` token, or assigner. This
can only be done if the variable is already defined though. So the
following code would throw an error that ``age`` isn't defined, but
the ``greeting`` variable would work fine.

.. code::

    String: greeting = "Hello world!";
    greeting = "Somewhere over the rainbow!";
    age = 42;

There are also four more assignment tokens that can be used. The
``+=`` and ``-=`` will add or subtract that value from the variable.
The ``++`` and ``--`` will add or subtract exactly 1 from the value
of the variable. These operations do not work on strings, only numbers.

The size of the value might matter sometimes. The default is a ``double
word``, or 32-bit, value. You may also specify a ``word``, 16-bit value,
or ``byte``, 8-bit value. Use these keywords in front of the value, after
the assignment token. For example: ``money = word 65536;`` will assign
the maximum value to ``money``. Thus, ``money = byte 260;``, which is 4
over the maximum of a byte (256) and will either fail or wrap around to 4.
Needless to say it will do some wacky things, and is generally avoided by
using double words unless needed.

Math
~~~~

The other basic of programming languages is math. Basic level math
consists of addition, subtraction, multiplication, division, powers,
grouping, and order of operations. These are all included in Aurora and
can be used whenever numbers are involved. As such the addition,
subtraction, multiplication, division, and powers are used whenever the
following characters are used in that context, respectively. ``+``,
``-``, ``*``, ``/``, ``^``. Groups are defined by opening and closing
parentheses (``()``). For more complex math, there is a built-in
math library with more functions.

Functions
~~~~~~~~~

Functions are a large part of most programming languages. For older more
retro languages, labels are usually used, these however, can become
confusing and over crowded. Functions take an input and return an output
based on those inputs. Some functions might also have no input, or no
output.

Defining a Function
^^^^^^^^^^^^^^^^^^^

Functions are defined similarly to variables. The following format can
be used, where anything in the square brackets is replaced with their
described values.

.. code::

    func: [Function Name]>[Argument 1]::[Type], [Argument 2]::[Type...] => [Return Type];
    end;

The Function Name is used whenever the function is called or invoked.
The Argument(s) are required parameters to execute the function. And the
Return Type is the type of variable returned by the function. This may
be Void, saying that the function will not return a specific type. Also
note the ``end`` tag after the function definition. This is required so
that aurora can tell when to stop executing code from the function. It
will also stop executing code if a value is returned from the function.

A function’s parameters and return type may also be nothing. Parameters may
include optional or predefined values. The following is an example of a function
taking no arguments.

.. code::

    func: foo_bar> => Number;
        return 32;
    end;

This function, named “foo_bar”, can be called using ``foo_bar>;`` and will
return the number ``32``. The following is an example of a function with one
required, and one optional argument.

.. code::

    func: rainbows>colors::String{}, pretty::Number=1;
        for>Number: i=0, i?<len>colors<, i++;
          print>colors{i}+"-";
        println>"";
        if>pretty ?= 1;
          println>"It's a pretty rainbow.";
        else;
          println>"It's just a rainbow.";
    end;

Calling a Function
^^^^^^^^^^^^^^^^^^

A defined function may be called as well. If it isn't defined then it cannot
be called. For example in a completely empty file the function ``bar_bar``
does not exist. But, if it is defined prior to calling it, such as in the
following code, then it may be called.

.. code::

    func: bar_bar> => Void;
        println>"foo foo";
    end;

    bar_bar>;

Including Functions
^^^^^^^^^^^^^^^^^^^

In an empty aurora file, no functions are defined except one, ``include``.
The include function can "import" or "include" other functions into the file.
This helps with freeing space, and making things look nicer. There are also
predefined libraries which can be imported without any extra installation.
The full list can be found on the `Libraries`_ page, however the most basic
ones are the I/O library by name ``io``, and the String library by name ``string``.

In most of the previous example, the function ``print`` or ``println`` is
called. However, to do this the following line must be added to the top of the
page, ``include>io;``. This will "import" or "include" the I/O library so that
the functions ``print`` and ``println`` can be called later in the code.

.. _Types: http://auroracompiler.rtfd.io/en/latest/types.html
.. _Libraries: http://auroracompiler.rtfd.io/en/latest/libraries.html
