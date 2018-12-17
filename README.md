# Aurora Compiler

Aurora is a simple language aimed towards low level implementation with readability.
It was made for practice with compilers, and for an IT class.

## PLEASE NOTE

This project is currently overgoing a major rehaul.
Don't expect anything to be complete yet, as it is being completely rewriten.

## Current Progress

The following is a list of what has been completed, what is being worked on, and what is planned in the future.
Items in **bold** have been completed.
Items in plain text are in progress.
Items in *italics* are planned.

* *Lexer*
* *Parser*
* *Generator*
* *Syntax*
  * *Function Calls*
  * *Includes*
  * *Builtin Libraries*
  * *Math Operations*
  * *Function Definitions*
  * *Lists*
  * *Comparisons*
* *Error Handling*
* *Strong Variable Typing*

## Getting Started

Aurora compiler can be run using:

```
python compiler.py [filename] [optional flags]
```

`[filename]` is optional, and replaced by whichever file you want to compile.
The `.aurora` file will be compiled to a `.py` Python file.
The `-r` or `--run` flags are optional, and run the compiled program after compiling.
Note that all compiled Aurora files (`.py`) files are in the build directory from  the same level as the `compiler.py` file.
To run a compiled Aurora, `.py` file, use:

```
python [filename]
```

More can be found with the [aurora compiler documentation][2] on [Read the Docs][3].

### Prerequisites and Installing

Python is needed and can be found at their website, [Python.org][1].

## Built With

* [Python][1] - Development language
* [Read the Docs][3] - Documentation (using Sphinx framework)
* [A Brain][4] - Some programmer's brain, code doesn't just grow on trees.

## Contributing

If you would like to Contribute to this project, please do.
It's open source for a reason after all.
Simply submit a Pull Request or Issue here on Github.

## Authors

* **Preston Hager** - *Programmer* - [Github Profile](https://github.com/PrestonHager)

See also the list of [contributors](https://github.com/PrestonHager/AuroraCompiler/blob/master/CONTRIBUTORS.md) who participated in this project.

## License

This project is licensed under the GNU General Public License v3.0, see the [LICENSE](https://github.com/PrestonHager/AuroraCompiler/blob/master/LICENSE) file for details.

(C) Preston Hager 2018-2019

[1]: https://www.python.org
[2]: http://auroracompiler.readthedocs.io/en/latest
[3]: https://readthedocs.org
[4]: https://github.com/PrestonHager
