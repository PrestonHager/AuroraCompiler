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
    def string(self):
        return str(self.value)

__all__ = ["_aurora_var_string", "_aurora_var_number"]
