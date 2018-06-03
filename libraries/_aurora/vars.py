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

__all__ = ["_aurora_var_string", "_aurora_var_number"]
