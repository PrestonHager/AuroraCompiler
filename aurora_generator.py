# aurora_generator.py

from aurora_parser import AuroraParser

class AuroraGenerator:
    def __init__(self, code):
        self._parser = AuroraParser(code)
        self.generated_code = ""
        self._generate(self._parser.parsed_code["body"])
    
    def _generate(self, tokens):
        for token in tokens:
            if token["token_value"] == "include":
                self.generated_code += "from _aurora.{library_name} import *\n".format(library_name=token["children"][0]["token_value"])
            elif token["token_type"] == "function":
                self.generated_code += "_aurora_{function_name}({arguments})\n".format(function_name=token["token_value"], arguments=self._generate_arguments(token["children"]))
            elif token["token_type"] == "comment":
                self.generated_code += "# {comment}\n".format(comment=token["token_value"])
    
    def _generate_arguments(self, tokens):
        generated_code = ""
        for token in tokens:
            if token["token_type"] == "string":
                generated_code += ",\"{string}\"".format(string=token["token_value"])
        return generated_code.strip(",")
