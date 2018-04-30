# Plan

### What is "this" exactly?

The Aurora Compiler is just yet another compiler.
It's goal is to help me (the author) practice and learn writing compilers.
Eventually this will lead to making a compiler in either C or Assembly for my OS, [Startaste.](https://github.com/PrestonHager/Startaste)

------
### What technology is used?

This compiler is writen entirely in Python (because the client requested it), and will compiler to Python code as well.
GitHub is used for version control and releases, and Read the Docs is used for documentation.

------
### What are the features?

The Aurora Compiler includes a Lexer or Tokenizer which creates an array (list) of tokens for the parser.
The next item is a parser, it will put the tokens into a logical order for the generator.
Next up, the generator.
This will create Python code based on what the parser outputs and will then be executable by a Python compiler.

------
### Timeline?

* **Week 0:** The plan.
* **Week 1:** Define the language terminology and make an example file.
* **Week 2:** Create the lexer/tokenizer.
* **Week 3-4:** Create the parser.
* **Week 5:** Create the generator.
* **Week 6:** Debug week. Test as much as possible and find all the bugs and fix them.