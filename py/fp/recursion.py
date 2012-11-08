def get_name():
    name = raw_input()
    return name if len(name) >= 2 else get_name()

get_name()
