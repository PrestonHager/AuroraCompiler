# generator.py
# by Preston Hager
# for Aurora Compiler

from math import ceil

class Generator:
    def __init__(self, parser):
        """
        Creates a new Generator instance

        Parameters
        ----------
        parser : Parser
            Parser to link to the generator

        Returns
        -------
        Generator
            New Generator instance with previous parameters.
        """
        self.parser = parser
        self.constants = {"string": {}, "number": {}}
        self.variables = {"string": [], "number": []}
        self.generated_code = "; generated by Aurora Compiler by Preston Hager\n; https://github.com/PrestonHager/AuroraCompiler\n[BITS 32]\n\n"
        self.generated_code_end = ""

    def generate(self):
        """
        Generates new code from the parser's AST
        """
        for node in self.parser.ast.children:
            generated_code_tuple = self._generate(node)
            if len(generated_code_tuple[0]) > 1:
                self.generated_code += generated_code_tuple[0]
            if len(generated_code_tuple[1]) > 1:
                self.generated_code_end += generated_code_tuple[1]
        self.generated_code += "\n" + self.generated_code_end.strip()

    def _generate(self, node):
        generated = ""
        generated_end = ""
        if node.name == "COMMENT":
            generated += f"; {node.children[0].value.strip()}"
        elif node.name == "FUNCTION":
            children_dict = self._children_dictionary(node)
            name = children_dict["NAME"].value
            arguments = children_dict["ARGUMENTS"].children
            if name == "_asm":
                for argument in arguments:
                    if argument.name == "STRING":
                        generated += f"{argument.value}\n"
            else:
                generated += f"; Arguments: {arguments}\n"
                arg_number = 0
                for argument in arguments:
                    arg_number += 1
                    if argument.name == "STRING":
                        var, new = self._constant("string", argument.value)
                        generated += f"mov [_aurora_arg_buffer+{arg_number*4}], DWORD _aurora_string_{var}\n"
                        if new:
                            generated_end += f"_aurora_string_{var} db \"{argument.value}\", 0\n"
                    if argument.name == "NUMBER":
                        var, new = self._constant("number", argument.value)
                        generated += f"mov [_aurora_arg_buffer+{arg_number*4}], DWORD _aurora_number_{var}\n"
                        if new:
                            generated_end += f"_aurora_number_{var} dd {argument.value}\n"
                generated += f"call {name}"
        elif node.name == "FOR":
            children_dict = self._children_dictionary(node)
            initialization = children_dict["INITIALIZATION"]
            condition = children_dict["CONDITION"]
            loop = children_dict["LOOP"]
            generated += f"; FOR: {node.children}"
        elif node.name == "VARIABLE_DEFINITION":
            children_dict = self._children_dictionary(node)
            type = children_dict["TYPE"].value
            name = children_dict["NAME"].value
            if type == "STRING":
                value = "NULL"
                if name in self.variables["string"]:
                    for i in range(ceil(len(value)/4)):
                        generated += f"; {i}\n"
                else:
                    self.variables["string"].append(name)
                    generated_end += f"{name} db \"{value}\"\n"
            elif type == "NUMBER":
                value = self._generate_value(children_dict["VALUE"].children[0])
                if name in self.variables["number"]:
                    gen_value = value
                    generated += f"{gen_value[0].strip()}\nmov [{name}], eax\n"
                    generated_end == gen_value[1]
                else:
                    self.variables["number"].append(name)
                    generated_end += f"{name} dd 0\n"
        elif node.name == "FUNCTION_DEFINTION":
            children_dict = self._children_dictionary(node)
            name = children_dict["NAME"].value
            parameters = children_dict["PARAMETERS"].children
            code = children_dict["CODE"].children
            generated += f"; {name}: {parameters}\n{name}:\n\tpusha\n"
            for line in code:
                generated_line = self._generate(line)
                generated += "\t" + "\n\t".join(generated_line[0].split("\n")).strip() + "\n"
                generated_end += generated_line[1]
            generated += f"\t.done:\n\tpopa\n\tret\n"
        elif node.name == "INCLUDE":
            children_dict = self._children_dictionary(node)
            generated_end += f"%include \"{children_dict['FILE'].value}\"\n"
        return (generated.strip()+"\n", generated_end.strip()+"\n")

    def _generate_value(self, postfix):
        value = ""
        generated_end = ""
        number_stack = []
        print(postfix)
        for node in postfix.children:
            if node.name == "NUMBER" or node.name == "VARIABLE":
                number_stack.append(node)
            else:
                if value == "":
                    gen_var = self._generate_variable(number_stack.pop())
                    generated_end += gen_var[1]
                    value += f"mov eax, {gen_var[0]}\n"
                if node.name == "TIMES":
                    gen_var = self._generate_variable(number_stack.pop())
                    value += f"mov ebx, {gen_var[0]}\nmul ebx\n"
                elif node.name == "DIVIDE":
                    gen_var = self._generate_variable(number_stack.pop())
                    value += f"mov ebx, {gen_var[0]}\n"
                elif node.name == "PLUS":
                    gen_var = self._generate_variable(number_stack.pop())
                    value += f"mov ebx, {gen_var[0]}\nadd eax, ebx\n"
                elif node.name == "MINUS":
                    gen_var = self._generate_variable(number_stack.pop())
                    value += f"mov ebx, {gen_var[0]}\nsub eax, ebx\n"
        return (value, generated_end)

    def _generate_variable(self, variable):
        if variable.name == "VARIABLE":
            if variable.name in self.variables["number"]:
                return (f"[{variable.value}]", f"{variable.value} dd 0\n")
            return (f"[{variable.value}]", "")
        elif variable.name == "NUMBER":
            return (f"{variable.value}", "")
        else:
            raise ValueError

    def _children_dictionary(self, node):
        children_dictionary = {}
        for child in node.children:
            children_dictionary[child.name] = child
        return children_dictionary

    def _constant(self, type, value):
        new = False
        if value not in self.constants[type]:
            new = True
            if len(self.constants[type]) < 1:
                self.constants[type][value] = 0
            else:
                self.constants[type][value] = max(self.constants[type].values())+1
        return (self.constants[type][value], new)
