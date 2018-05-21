Libraries
=========

There are three different types of libraries. Predefined libraries,
are already defined by the aurora language, and are included without
having to do extra work. User libraries, are defined by you, the
programmer, and can be included in any local file. Community libraries,
are any user libraries that has been made by another programmer, or
found from another source, such as the internet.

Predefined Libraries
~~~~~~~~~~~~~~~~~~~~

The following is a list of predefined libraries, their purpose, and
short list of their functions. More for each library can be found in
their documentation.

+ I/O Library - used for input and output operations. ``print``, ``println``.
+ Math Library - used for higher level math operations. ``sqrt``, ``round``, ``pow``, ``fib``, ``abs``.

User Libraries
~~~~~~~~~~~~~~

A programmer may also define their own library for use in local code.
To create a library, a folder with the library name must be present.
For example if the library ``greetings`` was to be defined then a
folder with the name ``greetings`` will be created. The folder must
be located in the ``libraries/user`` folder of the aurora installation
directory. The ``greetings`` folder must contain an ``config.json`` file
and any functions defined in the library in one or more files. The config
file will contain configurations for each function, what file they're in,
and what the call name is. The following might be an example of the
``greeting`` library.

.. code::
    
    {
    "bye": {
        "file": "farewells.aurora",
        "function": "bye"
    },
    "hi": {
        "file": "salutations.aurora",
        "function": "hi"
    },
    "hello": {
        "file": "salutations.aurora",
        "function": "hello"
    }
    }

The functions are usually in in alphabetical order. The sturcture could
be defined as so:

.. code::

    {
    "function_name": {
        "file": "filename.aurora",
        "function": "function_name_in_file"
    }
    }

The ``salutations.aurora`` file then might look like so:

.. code::
    
    include>io;
    
    func: hello>String name => Void;
        print>"Hello, ";
        print>name;
        println>"!";
    end;
    
    func: hi> => Void;
        println>"Hi there.";
    end;

And the ``farewells.aurora`` file might look as follows:

.. code::
    
    include>io;
    
    func: bye>String name => Void;
        print>"Good bye, ";
        print>name;
        println>".";
    end;

This will all create a library that can be called with ``include>greetings;``
and then the ``hello``, ``hi``, and ``bye`` functions can be called.

Community Libraries
~~~~~~~~~~~~~~~~~~~

The community can also put together libraries. To install on of these
download the library and put it in the ``libraries/user`` folder like
you would if you were creating a library. Then you can use any of those
functions in your aurora files after including them.
