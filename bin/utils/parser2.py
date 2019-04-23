# parser.py
# by Preston Hager
# for Aurora Compiler

import re

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.ast = ASTNode("TOP_LEVEL")
        self.argument_lengths = {"STRING": 0, "INTEGER": 0, "FLOAT": 0, "ID": 0, "STRING-PARAMETER": 0, "NUMBER-PARAMETER": 0, "INDEX": 0, "POINTER": 0}
        self.variables = {}
        self.local_variables = {}
        self.local_function = [False, ""]
        self.for_loop = False

    def parse(self):
        tokens = []
        include_nodes = []
        definition_nodes = []
        for token in self.lexer.lexed_code:
            tokens.append(token)
            if token["id"] == "ENDLINE":
                node, is_include, is_definition = self._parse_line(tokens)
                if is_include:
                    include_nodes.append(node)
                elif is_definition:
                    definition_nodes.append(node)
                else:
                    self.ast.add_child(node)
                tokens = []
        self.ast.add_child(ASTNode("EOF"))
        for node in include_nodes + definition_nodes:
            self.ast.add_child(node)
        del self.argument_lengths["ID"]
        self.ast.add_child(ASTNode("ARG_BUFFERS").add_children(*[ASTNode("ARG_BUFFER").add_child(ASTNode("NAME").add_child(ASTValue(arg))).add_child(ASTNode("LENGTH").add_child(ASTValue(self.argument_lengths[arg]))) for arg in self.argument_lengths]))

    def _parse_line(self, tokens):
        i = 0
        for i in range(len(tokens)):
            token = tokens[i]
            if token["id"] == "EQUALS":
                name = self._parse_line(tokens[:i])[0][0]
                value = self._parse_line(tokens[i+1:])[0]
                if type(value) == type([]):
                    value = value[0]
                print(name, value)
                return (ASTNode("ASIGNMENT").add_child(
                        ASTNode("VARIABLE").add_child(
                            name
                        )).add_child(
                        ASTNode("VALUE").add_child(
                            value
                        )), False, False)
            elif token["id"] == "FUNC_DEF":
                if tokens[i+1]["id"] != "SPACE":
                    raise ParserException("Expected a space after function declaration, `{code}`. At {pos}".format(code=''.join([t["val"] for t in tokens[i:]]), pos=', '.join([str(p) for p in tokens[i]["pos"]])))
                elif tokens[i+2]["id"] != "WORD":
                    raise ParserException("Expected a function name, `{code}`. At {pos}".format(code=''.join([t["val"] for t in tokens[i:]]), pos=', '.join([str(p) for p in tokens[i]["pos"]])))
                elif tokens[i+3]["id"] != "FUNC":
                    raise ParserException("Expected `>` after function name, `{code}`. At {pos}".format(code=''.join([t["val"] for t in tokens[i:]]), pos=', '.join([str(p) for p in tokens[i]["pos"]])))
                name = tokens[i+2]["val"]
                self.local_function = [True, name]
                parameters = self._parse_line(tokens[i+4:])[0]
                self.local_variables[name] = {}
                for parameter in parameters:
                    self.local_variables[name][parameter.children[0].value] = parameter.type.split("-")[0]
                return (ASTNode("FUNCTION-DEFINITION").add_child(
                        ASTNode("PARAMETERS").add_children(
                            *parameters)
                        ).add_child(
                        ASTNode("NAME").add_child(
                            ASTValue(name))
                        ), False, False)
            elif token["id"] == "FUNC":
                name = tokens[i-1]["val"]
                if name == "for":
                    self.for_loop = True
                    self.local_variables["for"] = {}
                    for_start = self._parse_line(tokens[i+1:i+8])[0]
                    self.local_variables["for"][for_start.children[0].children[0].value] = for_start.type.split("-")[0]
                    if self.local_function[0]:
                        self.local_variables[self.local_function[1]][for_start.children[0].children[0].value] = for_start.type.split("-")[0]
                    else:
                        self.variables[for_start.children[0].children[0].value] = for_start.type.split("-")[0]
                    try:
                        arg1, arg2 = [i for (y, i) in zip(tokens[i:], range(len(tokens[i:]))) if "," == y["val"]]
                    except:
                        raise ParserException("Not enough arguments passed to for loop, `{code}`. At {pos}".format(code=''.join([t["val"] for t in tokens[i-1:]]), pos=', '.join([str(p) for p in tokens[i]["pos"]])))
                    arguments = [self._parse_line(tokens[i+1:i+arg1])[0]]
                    arguments.append(self._parse_line(tokens[arg1+2:i+arg2])[0])
                    arguments += self._parse_line(tokens[i+arg2:])[0]
                    return (ASTNode("FUNCTION").add_child(
                            ASTNode("ARGUMENTS").add_children(
                                *arguments)
                            ).add_child(
                            ASTNode("NAME").add_child(
                                ASTValue("for"))
                            ), False, False)
                arguments = self._parse_line(tokens[i+1:])[0]
                if type(arguments) != type([]):
                    arguments = [arguments]
                elif name != "include":
                    for arg in range(len(arguments)):
                        if arguments[arg].type != "ID":
                            continue
                        variable = arguments[arg].children[0].value
                        if name == "for" and variable in self.local_variables["for"]:
                            continue
                        elif self.local_function[0] and variable in self.local_variables[self.local_function[1]]:
                            continue
                        elif variable in self.variables:
                            continue
                        raise ParserException("`{variable}` not defined, `{code}`. At {pos}".format(variable=variable, code=''.join([t["val"] for t in tokens[i-1:]]), pos=', '.join([str(p) for p in tokens[i]["pos"]])))
                return  (ASTNode("FUNCTION").add_child(
                        ASTNode("ARGUMENTS").add_children(
                            *arguments)
                        ).add_child(
                        ASTNode("NAME").add_child(
                            ASTValue(name))
                        ), name == "include", False)
            elif token["id"] == "STRING_VAR":
                equ = [i for (y, i) in zip(tokens[i+1:], range(len(tokens[i+1:]))) if "=" == y["val"]][0]
                name = self._parse_line(tokens[i+1:i+equ])[0][0].children[0].value.strip()
                value = self._parse_line(tokens[i+equ+2:])[0][0].children[0].value.strip()
                self.variables[name.value] = "STRING"
                return (ASTNode("STRING-VARIABLE").add_child(
                        ASTNode("NAME").add_child(
                            ASTValue(name)
                        )).add_child(
                        ASTNode("VALUE").add_child(
                            ASTValue(value))
                        ), False, True)
            elif token["id"] == "NUMBER_VAR":
                equ = [i for (y, i) in zip(tokens[i+1:], range(len(tokens[i+1:]))) if "=" == y["val"]][0]
                name = self._parse_line(tokens[i+1:i+equ])[0][0].children[0].value.strip()
                value = self._parse_line(tokens[i+equ+2:])[0][0].children[0].value.strip()
                self.variables[name] = "INTEGER"
                return (ASTNode("INTEGER-VARIABLE").add_child(
                        ASTNode("NAME").add_child(
                            ASTValue(name)
                        )).add_child(
                        ASTNode("VALUE").add_child(
                            ASTValue(value))
                        ), False, True)
            elif token["id"] == "RETURN":
                value = self._parse_line(tokens[i+1:])[0]
                if type(value) == type([]):
                    value = value[0]
                return (ASTNode("RETURN").add_child(
                            value
                        ), False, False)
        id_values = [{"val": "", "type": "ID", "matched": True, "pos": [0, 0]}]
        id_index = 0
        for i in range(len(tokens)):
            id_values[id_index]["pos"] = tokens[i]["pos"]
            if tokens[i]["id"] == "WORD":
                id_values[id_index]["val"] += tokens[i]["val"]
            elif tokens[i]["id"] == "SPACE":
                id_values[id_index]["val"] += " "
            elif tokens[i]["id"] == "STRING_DEF":
                if id_values[id_index]["type"] == "STRING":
                    if id_values[id_index]["matched"]:
                        raise ParserException("STRING was already closed, `{code}`. At {pos}".format(code=id_values[id_index]["val"], pos=', '.join([str(p) for p in tokens[i]["pos"]])))
                    id_values[id_index]["matched"] = True
                    id_values.append({"val": "", "type": "ID", "matched": True, "pos": [0, 0]})
                    id_index += 1
                else:
                    id_values[id_index] = {"val": "", "type": "STRING", "matched": False, "pos": id_values[id_index]["pos"]}
            elif tokens[i]["id"] == "EQUALS":
                id_values[id_index]["val"] = id_values[id_index]["val"].strip()
                id_values.append({"val": "", "type": "ID", "matched": True, "pos": [0, 0]})
                id_index += 1
            elif tokens[i]["id"] == "STRING_PARAMETER":
                id_values[id_index]["val"] = id_values[id_index]["val"].strip()
                id_values[id_index]["type"] = "STRING-PARAMETER"
                id_values.append({"val": "", "type": "ID", "matched": True, "pos": [0, 0]})
                id_index += 1
            elif tokens[i]["id"] == "NUMBER_PARAMETER":
                id_values[id_index]["val"] = id_values[id_index]["val"].strip()
                id_values[id_index]["type"] = "NUMBER-PARAMETER"
                id_values.append({"val": "", "type": "ID", "matched": True, "pos": [0, 0]})
                id_index += 1
            elif tokens[i]["id"] == "INDEX_START":
                id_values.append({"val": "", "type": "INDEX", "matched": False, "pos": tokens[i]["pos"]})
                id_index += 1
            elif tokens[i]["id"] == "INDEX_END":
                id_values[id_index]["matched"] = True
                id_values.append({"val": "", "type": "ID", "matched": True, "pos": [0, 0]})
                id_index += 1
            elif tokens[i]["id"] == "POINTER_START":
                id_values.append({"val": "", "type": "POINTER", "matched": False, "pos": tokens[i]["pos"]})
                id_index += 1
            elif tokens[i]["id"] == "POINTER_END":
                id_values[id_index]["matched"] = True
                id_values.append({"val": "", "type": "ID", "matched": True, "pos": [0, 0]})
                id_index += 1
            elif tokens[i]["id"] == "END_KEYWORD":
                if not self.for_loop:
                    self.local_function = [False, ""]
                return (ASTNode("END-TOKEN"), False, False)
            elif tokens[i]["id"] == "THEN_KEYWORD":
                return (ASTNode("THEN"), False, False)
            elif tokens[i]["id"] == "COMMA":
                pass
        if id_values[id_index]["val"] == "" and id_values[id_index]["type"] == "ID":
            id_values.pop()
        type_amount = {"STRING": 0, "INTEGER": 0, "FLOAT": 0, "ID": 0, "STRING-PARAMETER": 0, "NUMBER-PARAMETER": 0, "INDEX": 0, "POINTER": 0}
        for id in id_values:
            if re.match(r'0x[0-9]+', id["val"].strip()):
                id["type"] = "INTEGER"
            elif re.match(r'[0-9]+', id["val"].strip()):
                id["type"] = "INTEGER"
            elif re.match(r'[0-9]*\.[0-9]+', id["val"].strip()):
                id["type"] = "FLOAT"
            if id["type"] == "ID" and id["val"].strip() == "":
                id_values.pop(id_values.index(id))
                continue
            type_amount[id["type"]] += 1
            if not id["matched"]:
                raise ParserException("{type} was not closed, `{code}`. At {pos}".format(type=id["type"], code=id["val"], pos=', '.join([str(p) for p in id["pos"]])))
        self.argument_lengths = {k: max(type_amount[k], self.argument_lengths[k]) for k in type_amount}
        return ([ASTNode(id["type"]).add_child(ASTValue(id["val"])) for id in id_values], False, False)

class ASTNode:
    def __init__(self, type):
        self.type = type
        self.children = []
        self.children_amount = 0

    def __str__(self):
        return f"<ASTNode({self.children_amount}) `{self.type}`: {self.children}>"

    def __repr__(self):
        return self.__str__()

    def add_child(self, child):
        self.children.append(child)
        self.children_amount += 1
        return self

    def add_children(self, *children):
        for child in children:
            self.add_child(child)
        return self

class ASTValue:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"<ASTValue `{self.value}`>"

    def __repr__(self):
        return self.__str__()

class ParserException(Exception):
    pass
