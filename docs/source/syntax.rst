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
name must also not start with a digit (number). A value is contricted to
that variable’s type. For example if a variable’s type is ``Number``
then it must be an integer or float (a number). If the type is
``String`` then the value must be an array of characters defined by
``"[Value]"``. Notice the double quotation marks on either side of the
value.

A list of types with their expected values can be found on the `Types`_
page.

Math
~~~~

The other basic of programming languages is math. Basic level math
consists of addition, subtraction, multiplication, division, powers,
grouping, and order of operations. These are all included in Aurora and
can be used whenever numbers are involved. As such the addition,
subtraction, multiplication, division, and powers are used whenever the
following characters are used in that context, respectively. ``+``,
``-``, ``*``, ``/``, ``^``. Groups are defined by opening and closing
parentheses (``()``), or square brackets (``[]``). For more complex
math, there is a builtin math library with more functions.

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

    func: [Function Name]>[Argument 1]::[Type], [Arugment 2]::[Type...] => [Return Type];

The Function Name is used whenever the function is called or invoked.
The Arugment(s) are required parameters to execute the function. And the
Return Type is the type of variable returned by the function. This may
be Void, saying that the function will not return a specific type.

A function’s arguments/parameters may also be nothing, or include
optional or predefined values. The following is an example of a function
taking no arguments.

.. code::

    func: fooBar> => Number
        return 32

This function, named “fooBar”, can be called using ``foobar>;`` and will
return the number 32. The following is an example of a function with one
required, and one optional argument.

.. code::

    func: rainbows>colors::String{}, pretty::Number=1 => Void;
        for>Number:i=0, i ?< colors.length>, i=i+1;
        print>colors{i}+"-";
        println>"";
        if>pretty ?= 1;
        println>"It's a pretty rainbow.";
        else;
        println>"It's just a rainbow.";``

Calling a Function
^^^^^^^^^^^^^^^^^^

A defined function may be called as well. If it isn't defined then it cannot
be called. For example in a completely empty file the function ``barBar``
does not exist. But, if it is defined prior to calling it, such as in the
following code, then it may be called.

.. code::

    func: barBar> => Void;
        println>"fooFoo";
    
    barBar>;

Including Functions
^^^^^^^^^^^^^^^^^^^

In an empty aurora file, no functions are defiend except one, ``include``.
The include function can "import" or "include" other functions into the file.
This helps with freeing space, and making things look nicer. There are also
predefined librarys which can be imported without any extra installation.
The full list can be found on the `Libraries`_ page, however the most basic
ones are the I/O library by name ``io``, and the Math library by name ``math``.

In most of the previous example, the function ``print`` or ``println`` is
called. However, to do this the following line must be added to the top of the
page, ``include>io;``. This will "import" or "include" the I/O library so that
the functions ``print`` and ``println`` can be called later in the code.

.. _Types: https://auroracompiler.rtfd.io/en/latest/types.html
.. _Libraries: https://auroracompiler.rtfd.io/en/latest/libraries.html
