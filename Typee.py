import json

class Typee:


    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        self.size = len(fields) * 19


types = []


def search_type(name):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    if name not in files_json.keys():
        return -1
    return files_json[name]
    """
    listt = [x for x in types if x.name == name]
    return -1 if len(listt) == 0 else listt[0]
    """


# name is a string
# field is a list
def create_type(name, field):
    if search_type(name) != -1:
        return -1
    type = Typee(name, field)
    types.append(type)
    return type


def delete_type(name):
    type = search_type(name)
    if type != -1:
        types.remove(type)
        del type
    else:
        return -1


def list_types():
    return types


def inherit_type(name, source_name, field):
    source_type = search_type(source_name)
    if source_type == -1:
        return -1  # no such source type
    type = Typee(name, source_type.fields + field)
    types.append(type)
