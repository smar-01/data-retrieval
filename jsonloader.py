import json

def write_to_file(filename,dict):
    with open(filename, 'w') as file:
        json.dump(dict, file)
    return True

def read_from_file(filename):
    with open(filename, 'r') as file:
        large_dict = json.load(file)
        return large_dict