# lexer.py
# by Preston Hager
# for Aurora Compiler

class Lexer:
    def __init__(self, code, bin_dir):
        self.code = code
        self.lexed_code = []
        with open(bin_dir+"/bin/operations.txt", 'r') as f_in:
            cont = f_in.read().strip()
        self.operations = {l.split(":=")[0].strip(): l.split(":=")[1].strip().replace("\s", " ").replace("\\n", "\n") for l in cont.split("\n")}

    def lex(self):
        position = 0
        character_position = [1, 1]
        token = ""
        comment = False
        while position < len(self.code):
            token += self.code[position]
            if self.code[position] == "\n":
                token = ""
                character_position = [character_position[0]+1, 1]
            else:
                character_position[1] += 1
            if token == "//":
                comment = True
            if not comment:
                for opr in self.operations:
                    operation = self.operations[opr]
                    if ''.join(self.code[position:position+len(operation)]) == operation:
                        if len(token) > 1:
                            self.append_token("WORD", ''.join(token[:-len(operation)]), [character_position[0], character_position[1]-len(operation)-len(token)+1])
                        self.append_token(opr, operation, [character_position[0], character_position[1]-1])
                        position += len(operation)-1
                        character_position[1] += len(operation)-1
                        token = ""
                        break
            elif self.code[position] == "\n":
                comment = False
                token = ""
            position += 1

    def append_token(self, id, value, pos):
        self.lexed_code.append({"id": id, "val": value, "pos": pos})
