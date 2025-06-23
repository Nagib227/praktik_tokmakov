from db import create_db, find_matching_patterns

from Parse_console_args import Parse_console_args
from DataType import DataType


def get_args_pattern(argsJson):
    pattern = {}
    for i in argsJson.keys():
        pattern[i] = DataType(argsJson[i]).type

    return pattern

    
def main():
    create_db()

    
    argsJson = Parse_console_args()
    args_pattern = get_args_pattern(argsJson)

    results = find_matching_patterns(args_pattern)
    if results:
        print(results[0]["name"])
    else:
        print(args_pattern)
    

if __name__ == "__main__":
    main()
