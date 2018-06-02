# aurora_generator.py

# import statements
from aurora_parser import AuroraParser

class AuroraGenerator:
    # initalization of the generator
    def __init__(self, code):
        # takes the same input as parser, and lexer
        self._parser = AuroraParser(code)
        # default values
        self.generated_code = ""
        # generate code
        self._generate(self._parser.parsed_code)

    def _generate(self, parsed_code):
        tokens = parsed_code["body"] # get all the tokens
        # if string variable, or number varaible are required, import them
        if "string_variables" in parsed_code["initialized"]["required"] or "number_variables" in parsed_code["initialized"]["required"]:
            self.generated_code += "from _aurora.vars import *\n"
        for token in tokens: # generate a new line of code for each token (line) in the AST
            if token["token_type"] == "function": # if the token is function, then the Python code is `func(arguments)`
                if token["token_value"] == "include": # if the token is include, then the Python code is an import statement
                    self.generated_code += "from _aurora.{library_name} import *\n".format(library_name=token["children"][0]["token_value"])
                elif token["token_value"] in parsed_code["initialized"]["defined"]: # if it's been defined by the user, then use that name
                    self.generated_code += "{variable}.{function_name}({arguments})\n".format(variable=token["token_value"], function_name=token["children"][0], arguments=self._generate_arguments(token["children"][1:]))
                else: # otherwise, prepend `_aurora_` to it to call a builtin function (don't forget to include it)
                    self.generated_code += "_aurora_{function_name}({arguments})\n".format(function_name=token["token_value"], arguments=self._generate_arguments(token["children"]))
            elif token["token_type"] == "comment": # if the token is comment, then the Python code is `# comment`
                self.generated_code += "# {comment}\n".format(comment=token["token_value"])
            elif token["token_type"] == "string_variable": # if the token in string_variable, then the Python code is `var = _aurora_var_string(value)`
                if len(token["children"]) > 0: # if the value has been preset, then include the string in the arguments
                    self.generated_code += "{variable} = _aurora_var_string({string})\n".format(variable=token["token_value"], string=self._generate_arguments(token["children"]))
                else: # otherwise, just initalize the string as None
                    self.generated_code += "{variable} = _aurora_var_string()\n".format(variable=token["token_value"])
            elif token["token_type"] == "number_variable": # if the token is number_variable, then the Python code is `var = _aurora_var_number(value)`
                if len(token["children"]) > 0: # if the value has been preset, then include in the arugments
                    self.generated_code += "{variable} = _aurora_var_number({number})\n".format(variable=token["token_value"], number=self._generate_arguments(token["children"]))
                else: # otherwise, don't
                    self.generated_code += "{variable} = _aurora_var_number()\n".format(variable=token["token_value"])

    # generate arugments for functions
    def _generate_arguments(self, tokens):
        # takes the children of a function (mostly varaibles, and constants)
        generated_code = ""
        for token in tokens:
            if token["token_type"] == "string": # if the token type is a stirng, then the Python code is `"value"`
                generated_code += ",\"{string}\"".format(string=token["token_value"])
            elif token["token_type"] == "number": # if the token type is a number, then the Python code is the same as the value
                generated_code += ",{number}".format(number=token["token_value"])
            elif token["token_type"] == "variable": # if the token type is a variable, then the Python code is the same as the value
                if len(token["children"]) > 0:
                    generated_code += ",{variable}.{function}({arguments})".format(variable=token["token_value"], function=token["children"][0]["token_value"], arguments=self._generate_arguments(token["children"][1:]))
                else:
                    generated_code += ",{varaible}.get()".format(varaible=token["token_value"])
            elif token["token_type"] == "function": # if the token type is a funciton, then the Python code is `func(arguments)`
                function_name = token["token_value"]
                if function_name in self._parser.parsed_code["initialized"]["defined"]:
                    generated_code += ",{function_name}({child_variable})".format(function_name=function_name, child_variable=self._generate_arguments(token["children"]))
                else:
                    generated_code += ",_aurora_{function_name}({child_variable})".format(function_name=function_name, child_variable=self._generate_arguments(token["children"]))
        return generated_code.strip(",")
