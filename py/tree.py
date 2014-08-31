# encoding: utf-8

def pretty(d, indent=0):
    for key, value in d.items():
        line = "\t" * indent + str(key)
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            line += "\t" * (indent+1) + str(value)
        print(line)

pretty({"a": "b", "c": {"a": "c"}})
