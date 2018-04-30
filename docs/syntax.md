# Syntax

### Definitions

The basis of all programming languages is definitions and math.
To define a variable in Aurora is simple.
You must know the *type*, the *name*, and a *value*.
Definition is then as follows.
```
[Type]: [Name] = [Value]
```
There are many types, and one can also create their own variable type.
Names consist of standard ASCII characters, underscores, and digits;
a name must also not start with a digit (number).
A value is contricted to that variable's type.
For example if a variable's type is `Number` then it must be an integer or float (a number).
If the type is `String` then the value must be an array of characters defined by `"[Value]"`.
Notice the double quotation marks on either side of the value.

A list of types with their expected values can be found on the [Types page.](http://auroracompiler.rtfd.io/en/latest/types)

-------
### Math

The other basic of programming languages is math.
Basic level math consists of addition, subtraction, multiplication, division, powers, grouping, and order of operations.
These are all included in Aurora and can be used whenever numbers are involved.
As such the addition, subtraction, multiplication, division, and powers are used whenever the following characters are used in that context, respectively. `+`, `-`, `*`, `/`, `^`. 
Groups are defined by opening and closing parentheses (`()`), or square brackets (`[]`).
For more complex math, there is a builtin math library with more functions. 

------
### Functions

Functions are a large part of most programming languages.
For older more retro languages, labels are usually used, these however, can become confusing and over crowded.
Functions take an input and return an output based on those inputs.
Some functions might also have no input, or no output.
