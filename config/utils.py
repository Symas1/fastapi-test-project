from yaml import safe_load


def load_conf(filepath):
    with open(filepath, 'r') as file:
        return safe_load(file)
