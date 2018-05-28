# aurora_generator.py

from aurora_parser import AuroraParser

class AuroraGenerator:
    def __init__(self, code):
        self._parser = AuroraParser(code)
        self.generated_code = ""
        self._generate(self._parser.parsed_code)

    def _generate(self, parsed_code):
        tokens = parsed_code["body"]
        if "string_variables" in parsed_code["initialized"]["required"] or "number_variables" in parsed_code["initialized"]["required"]:
            self.generated_code += "from _aurora.vars import *\n"
        for token in tokens:
            if token["token_value"] == "include":
                self.generated_code += "from _aurora.{library_name} import *\n".format(library_name=token["children"][0]["token_value"])
            elif token["token_type"] == "function":
                if token["token_value"] in parsed_code["initialized"]["defined"]:
                    # Unfinished.
                    self.generated_code += "{variable}.{function_name}({arguments})\n".format(variable=token["token_value"], function_name=token["children"][0], arguments=self._generate_arguments(token["children"]))
                else:
                    self.generated_code += "_aurora_{function_name}({arguments})\n".format(function_name=token["token_value"], arguments=self._generate_arguments(token["children"]))
            elif token["token_type"] == "comment":
                self.generated_code += "# {comment}\n".format(comment=token["token_value"])
            elif token["token_type"] == "string_variable":
                if len(token["children"]) > 0:
                    self.generated_code += "{variable} = _aurora_var_string({string})\n".format(variable=token["token_value"], string=self._generate_arguments(token["children"]))
                else:
                    self.generated_code += "{variable} = _aurora_var_string()\n".format(variable=token["token_value"])
            elif token["token_type"] == "number_variable":
                if len(token["children"]) > 0:
                    self.generated_code += "{variable} = _aurora_var_number({number})\n".format(variable=token["token_value"], number=self._generate_arguments(token["children"]))
                else:
                    self.generated_code += "{variable} = _aurora_var_number()\n".format(variable=token["token_value"])

    def _generate_arguments(self, tokens):
        generated_code = ""
        for token in tokens:
            if token["token_type"] == "string":
                generated_code += ",\"{string}\"".format(string=token["token_value"])
            if token["token_type"] == "number":
                generated_code += ",{number}".format(number=token["token_value"])
            elif token["token_type"] == "variable":
                if len(token["children"]) > 0:
                    generated_code += ",{variable}.{child_variable}".format(variable=token["token_value"], child_variable=self._generate_arguments(token["children"]))
                else:
                    generated_code += ",{variable}.get()".format(variable=token["token_value"])
        return generated_code.strip(",")
