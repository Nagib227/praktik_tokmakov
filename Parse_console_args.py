import sys

def Parse_console_args():
    args = {}
    for i in sys.argv[1:]:
        name, value = i.split("=")
        name = name.strip()[2:]
        value = value.strip()
        if not (args.get(name, None) is None):
            raise "два аргумента с одним именем"
        args[name] = value
    return args
