# generator.py
# by Preston Hager
# for Aurora Compiler

class Generator:
    def __init__(self, parser):
        self.parser = parser
        self.generated_code = "; generated by Aurora Compiler by Preston Hager\n; https://github.com/PrestonHager/AuroraCompiler\n\n"
        self.variables = {}
        self.variable_index = 0

    def generate(self):
        for node in self.parser.ast.children:
            self.generated_code += self._generate_node(node) + "\n"
        for variable in self.variables:
            self.generated_code += f"_VAR_{self.variables[variable]} db \"{variable}\", 0\n"
        self.generated_code = self.generated_code.strip() + "\n_aurora_end:"

    def _generate_node(self, node):
        generated = ""
        if node.type == "FUNCTION":
            arguments = []
            name = None
            for child in node.children:
                if child.type == "ARGUMENTS":
                    arguments += child.children
                if child.type == "NAME":
                    name = child.children[0].value
            if name == "include":
                if arguments[0].type == "ID":
                    generated += f"%include \"lib/_aurora_{arguments[0].children[0].value}.asm\""
                else:
                    generated += f"%include \"lib/{arguments[0].children[0].value}.asm\""
            else:
                for argument in arguments:
                    if argument.type == "STRING":
                        if argument.children[0].value in self.variables:
                            generated += f"mov si, _VAR_{self.variables[argument.children[0].value]}\npush si\n"
                        else:
                            self.variables[argument.children[0].value] = self.variable_index
                            generated += f"mov si, _VAR_{self.variable_index}\npush si\n"
                            self.variable_index += 1
                generated += f"mov bx, {len(arguments)}\ncall _aurora_{name}"
        elif node.type == "EOF":
            generated += "jmp {}".format("_aurora_end")
        return generated
