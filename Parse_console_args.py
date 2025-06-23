import sys

class DuplicateArgumentError(Exception):
    pass

def Parse_console_args():
    args = {}
    for i in sys.argv[1:]:
        name, value = i.split("=")
        name = name.strip()[2:]
        value = value.strip()
        if not (args.get(name, None) is None):
            raise DuplicateArgumentError(f"Два аргумента с одним именем: {name}")
        args[name] = value
    return args
