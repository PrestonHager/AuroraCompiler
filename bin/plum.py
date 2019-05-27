import sys

class Plum:
    def get_args(self, argv, defaults):
        """
        Gets the argument variables from the command line and breaks them up into dictionary values that can be worked with.

        Parameters
        ----------
        argv : Dictionary
            A dictionary of arguments with values of type list.
        defaults : Dictionary
            A dictionary of values of either type plum.Integer or plum.String.

        Example:
            plum.get_args({"file": ["-f", "--file"], {"verbose": ["-v"]}}, {"file": plum.String("myfile.txt")})
        """
        args = {key: (defaults[key].value if key in defaults else False) for key in argv}
        ARG = ""
        for a in sys.argv:
            if ARG != "":
                args[ARG] = defaults[ARG].format(a)
                ARG = ""
            for arg in argv:
                if a in argv[arg]:
                    if args[arg] == False:
                        args[arg] = True
                    else:
                        ARG = arg
        return args

class Integer:
    """
    Used to assign a default value to an argument.

    Parameters
    ----------
    value : Integer
        The default value for the integer argument.
    """
    def __init__(self, value):
        self.value = value
        self.ntype = "<class 'int'>"

    def format(self, value):
        try:
            return int(value)
        except ValueError:
            print("ValueError: invalid literal for int() with base 10: '{}'. Used default: '{}'".format(value, self.value))
            return self.value

class String:
    """
    Used to assign a default value to an argument.

    Parameters
    ----------
    value : String
        The default value for the string argument.
    """
    def __init__(self, value):
        self.value = value
        self.ntype = "<class 'str'>"

    def format(self, value):
        return str(value)

_inst = Plum()
get_args = _inst.get_args
__all__ = ["Integer", "String", "get_args"]
