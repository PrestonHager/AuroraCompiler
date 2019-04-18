# parser.py
# by Preston Hager
# for Aurora Compiler

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.ast = ASTNode("TOP_LEVEL")
        self.argument_lengths = {"STRING": 0, "INTEGER": 0, "FLOAT": 0, "ID": 0}
        self.variables = {}

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
        print(tokens)
        for i in range(len(tokens)):
            token = tokens[i]
            if token["id"] == "FUNC":
                name = tokens[i-1]["val"]
                arguments = self._parse_line(tokens[i+1:])[0]
                if type(arguments) != type([]):
                    arguments = [arguments]
                elif name != "include":
                    for arg in arguments:
                        variable = arg.children[0].value
                        if arg.type == "ID" and variable not in self.variables:
                            raise ParserException("`{variable}` not defined, `{code}`. At {pos}".format(variable=variable, code=''.join([t["val"] for t in tokens[i-1:]]), pos=', '.join([str(p) for p in tokens[i]["pos"]])))
                return  (ASTNode("FUNCTION").add_child(
                        ASTNode("ARGUMENTS").add_children(
                            *arguments)
                        ).add_child(
                        ASTNode("NAME").add_child(
                            ASTValue(name))
                        ), name == "include", False)
            elif token["id"] == "STRING_VAR":
                parsed_line = self._parse_line(tokens[i+1:])[0]
                name = parsed_line[0].children[0]
                value = parsed_line[1]
                self.variables[name.value] = "STRING"
                return (ASTNode("STRING-VARIABLE").add_child(
                        ASTNode("NAME").add_child(
                            name
                        )).add_child(
                        ASTNode("VALUE").add_child(
                            value)
                        ), False, True)
            elif token["id"] == "NUMBER_VAR":
                parsed_line = self._parse_line(tokens[i+1:])[0]
                name = parsed_line[0].children[0]
                value = parsed_line[1]
                self.variables[name.value] = "INTEGER"
                return (ASTNode("INTEGER-VARIABLE").add_child(
                        ASTNode("NAME").add_child(
                            name
                        )).add_child(
                        ASTNode("VALUE").add_child(
                            value)
                        ), False, True)
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
            elif tokens[i]["id"] == "COMMA":
                pass
                # id_index += 1
                # id_values.append({"val": "", "type": "ID", "matched": True, "pos": [0, 0]})
        if id_values[id_index]["val"] == "" and id_values[id_index]["type"] == "ID":
            id_values.pop()
        type_amount = {"STRING": 0, "INTEGER": 0, "FLOAT": 0, "ID": 0}
        for id in id_values:
            try:
                float(id["val"].strip())
                id["val"] = id["val"].strip()
                if "." in id["val"]:
                    id["type"] = "FLOAT"
                else:
                    id["type"] = "INTEGER"
            except:
                pass
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
