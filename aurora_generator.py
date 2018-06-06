# aurora_generator.py

# import statements
from aurora_parser import AuroraParser
import json
import os.path
import sys

class AuroraGenerator:
    # initalization of the generator
    def __init__(self, code):
        # takes the same input as parser, and lexer
        self._parser = AuroraParser(code)
        self.aurora_libraries = os.path.join(os.path.abspath(sys.argv[0]), "..", "libraries").replace("\\","\\\\")
        # generate code
        self.generated_code = self._generate(self._parser.parsed_code["body"], self._parser.parsed_code["initialized"])

    def _generate(self, tokens, initialized, indent="", imports=True):
        generated_code = ""
        # if string variable, or number varaible are required, import them
        if imports:
            generated_code = "import sys\nsys.path.append(\"{aurora_libraries}\")\n".format(aurora_libraries=self.aurora_libraries)
            if "string_variables" in initialized["required"] or "number_variables" in initialized["required"]:
                generated_code += "from _aurora.vars import *\n"
        for token in tokens: # generate a new line of code for each token (line) in the AST
            if token["token_type"] == "function": # if the token is function, then the Python code is `func(arguments)`
                if token["token_value"] == "include": # if the token is include, then the Python code is an import statement
                    if imports:
                        generated_code += "{indent}from _aurora.{library_name} import *\n".format(indent=indent, library_name=token["children"][0]["token_value"])
                elif token["token_value"] in initialized["defined"]: # if it's been defined by the user, then use that name
                    generated_code += "{indent}{function_name}({arguments})\n".format(indent=indent, function_name=token["token_value"], arguments=self._generate_arguments(token["children"]))
                else: # otherwise, prepend `_aurora_` to it to call a builtin function (don't forget to include it)
                    generated_code += "{indent}_aurora_{function_name}({arguments})\n".format(indent=indent, function_name=token["token_value"], arguments=self._generate_arguments(token["children"]))
            elif token["token_type"] == "comment": # if the token is comment, then the Python code is `# comment`
                generated_code += "{indent}# {comment}\n".format(indent=indent, comment=token["token_value"])
            elif token["token_type"] == "function_definition": # if the token is a function definition, then the Python code is `def func(args):...`
                generated_code += "{indent}def {function}({arguments}):\n  global {vars}\n{code}\n".format(indent=indent, function=token["token_value"], arguments=self._generate_function_arguments(token["children"][0]["children"]), vars=self._get_vars(initialized), code=self._generate(token["children"][2]["children"], initialized, indent+"  ", False))
            elif token["token_type"] == "string_variable": # if the token in string_variable, then the Python code is `var = _aurora_var_string(value)`
                if len(token["children"]) > 0: # if the value has been preset, then include the string in the arguments
                    generated_code += "{indent}{variable} = {string}\n".format(indent=indent, variable=token["token_value"], string=self._generate_arguments(token["children"]))
                else: # otherwise, just initalize the string as None
                    generated_code += "{indent}{variable} = _aurora_var_string()\n".format(indent=indent, variable=token["token_value"])
            elif token["token_type"] == "number_variable": # if the token is number_variable, then the Python code is `var = _aurora_var_number(value)`
                if len(token["children"]) > 0: # if the value has been preset, then include in the arugments
                    generated_code += "{indent}{variable} = {number}\n".format(indent=indent, variable=token["token_value"], number=self._generate_arguments(token["children"]))
                else: # otherwise, don't
                    generated_code += "{indent}{variable} = _aurora_var_number()\n".format(indent=indent, variable=token["token_value"])
        return generated_code

    # generate the arguments for defined functions
    def _generate_function_arguments(self, tokens):
        generated_code = ""
        for token in tokens:
            if token["token_type"] == "string_variable":
                if len(token["children"]) > 0:
                    generated_code += ",{name}={value}".format(name=token["token_value"], value=self._generate_arguments([token["children"][0]]))
                else:
                    generated_code += ",{name}".format(name=token["token_value"])
            if token["token_type"] == "number_variable":
                if len(token["children"]) > 0:
                    generated_code += ",{name}={value}".format(name=token["token_value"], value=self._generate_arguments([token["children"][0]]))
                else:
                    generated_code += ",{name}".format(name=token["token_value"])
        return generated_code.strip(",")

    # generate arugments for functions
    def _generate_arguments(self, tokens):
        # takes the children of a function (mostly varaibles, and constants)
        generated_code = ""
        for token in tokens:
            if token["token_type"] == "string": # if the token type is a stirng, then the Python code is `"value"`
                generated_code += ",_aurora_var_string(\"{string}\")".format(string=token["token_value"])
            elif token["token_type"] == "plus": # if the token type is a plus sign, then the Python code is `num + num2`
                generated_code += ",_aurora_var_number({number}+{number2})".format(number=token["children"][0]["token_value"], number2=token["children"][1]["token_value"])
            elif token["token_type"] == "subtract": # if the token type is a minus sign, then the Python code is `num - num2`
                generated_code += ",_aurora_var_number({number}-{number2})".format(number=token["children"][0]["token_value"], number2=token["children"][1]["token_value"])
            elif token["token_type"] == "multiply": # if the token type is a multiply sign, then the Python code is `num * num2`
                generated_code += ",_aurora_var_number({number}*{number2})".format(number=token["children"][0]["token_value"], number2=token["children"][1]["token_value"])
            elif token["token_type"] == "divide": # if the token type is a divide sign, then the Python code is `num / num2`
                generated_code += ",_aurora_var_number({number}/{number2})".format(number=token["children"][0]["token_value"], number2=token["children"][1]["token_value"])
            elif token["token_type"] == "number": # if the token type is a number, then the Python code is the same as the value
                generated_code += ",_aurora_var_number({number})".format(number=token["token_value"])
            elif token["token_type"] == "variable": # if the token type is a variable, then the Python code is the same as the value
                if len(token["children"]) > 0:
                    generated_code += ",{variable}.{function}({arguments})".format(variable=token["token_value"], function=token["children"][0]["token_value"], arguments=self._generate_arguments(token["children"][1:]))
                else:
                    generated_code += ",{varaible}".format(varaible=token["token_value"])
            elif token["token_type"] == "function": # if the token type is a funciton, then the Python code is `func(arguments)`
                function_name = token["token_value"]
                if function_name in self._parser.parsed_code["initialized"]["defined"]:
                    generated_code += ",{function_name}({child_variable})".format(function_name=function_name, child_variable=self._generate_arguments(token["children"]))
                else:
                    generated_code += ",_aurora_{function_name}({child_variable})".format(function_name=function_name, child_variable=self._generate_arguments(token["children"]))
        return generated_code.strip(",")

    def _get_vars(self, _vars):
        generated_code = ""
        for var in _vars["all"]:
            if var in _vars["defined"]:
                generated_code += ",{var}".format(var=var)
            else:
                generated_code += ",_aurora_{var}".format(var=var)
        return generated_code.strip(",")
