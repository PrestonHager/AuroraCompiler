# Aurora Variables library

class _aurora_var:
    def __init__(self, value=None):
        self.value = value

    def set(self, value):
        self.value = value
    def get(self):
        return self.value

    def __repr__(self):
        return str(self.value)

class _aurora_var_string(_aurora_var):
    pass

class _aurora_var_number(_aurora_var):
    def __init__(self, value=None):
        super(_aurora_var_number, self).__init__(value)
        self.string_value = _aurora_var_string(str(self.value))

    def string(self):
        return self.string_value

class _aurora_var_list(_aurora_var):
    def __init__(self, type, value=None):
        super(_aurora_var_list, self).__init__(value)
        self.type = type

    def push(self, value):
        self.value.append(value)
    def pop(self):
        value = self.value[-1]
        self.value.pop()
        return value
    def get(self, index, index2):
        return self.value[index:index2+1]
    def get_all(self):
        return self.value

__all__ = ["_aurora_var_string", "_aurora_var_number", "_aurora_var_list"]
