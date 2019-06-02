# Aurora Compiler

![Documentation Status](https://readthedocs.org/projects/auroracompiler/badge/?version=latest)
![GitHub License](https://img.shields.io/github/license/PrestonHager/AuroraCompiler.svg?color=blue)
![Custom badge](https://img.shields.io/endpoint.svg?color=blue&label=progress&url=https%3A%2F%2Fscript.google.com%2Fmacros%2Fs%2FAKfycbyMtmJktHmceU6x_Fam5XdEpx9tijrwZavXOy-cV7SifSqTP1o%2Fexec)

Aurora is a simple language aimed towards low level implementation with readability.
It was made for practice with compilers, and for an IT class.
Later it was adopted for [Startaste][5], an OS developed by I, [Preston Hager][4].

-----

## Current Progress

The following is a list of what has been completed, what is being worked on, and what is planned in the future.
Items in **bold** have been completed.
Items in plain text are in progress.
Items in *italics* are planned.

* **Lexer**
* Parser
* Generator
* Syntax
  - **Variable Definitions**
  - **Function Calls**
  - **Includes**
  - Builtin Libraries
  - *Math Operations*
  - **Function Definitions**
  - *Lists*
  - *Comparisons*
* *Error Handling*
* Strong Variable Typing

-----

## Getting Started

Aurora compiler can be run using:

```
aurora [filename] [optional flags]
```

`[filename]` is the file that you want to compile.
It can be either an absolute or a relative path.
The `.aurora` file will be compiled to a `.bin` file after going through nasm as a `.asm` file.
Note that all compiled Aurora files (`.bin`) files are in the build directory from original file.

More information can be found with the [aurora compiler documentation][2] on [Read the Docs][3].

### Prerequisites and Installing

Python is needed and can be found at their website, [Python.org][1].
NASM is needed to compile to `.asm` files, found at [nasm.us][6].

To make it easier to compiler files, install the `aurora` command.
To do this add it to the PATH environment variables.
Please note, you must be in the AuroraCompiler directory to do this.
Use the following command to do this:

```
export PATH=$PATH:$(pwd)/bin
```

-----

## Built With

* [Python][1] - Development language
* [NASM][6] - Assembler
* [Read the Docs][3] - Documentation (using Sphinx framework)
* [A Brain][4] - Some programmer's brain....

-----

## Contributing

If you would like to Contribute to this project, please do.
It's open source for a reason after all.
Simply submit a Pull Request or Issue here on Github.

-----

## Authors

* **Preston Hager** - *Programmer* - [Github Profile](https://github.com/PrestonHager)

See also the list of [contributors](https://github.com/PrestonHager/AuroraCompiler/blob/master/CONTRIBUTORS.md) who participated in this project.

-----

## License

This project is licensed under the GNU General Public License v3.0, see the [LICENSE](https://github.com/PrestonHager/AuroraCompiler/blob/master/LICENSE) file for details.

(C) Preston Hager 2018-2019

[1]: https://www.python.org
[2]: http://auroracompiler.readthedocs.io/en/latest
[3]: https://readthedocs.org
[4]: https://github.com/PrestonHager
[5]: https://github.com/PrestonHager/Startaste
[6]: https://www.nasm.us/
