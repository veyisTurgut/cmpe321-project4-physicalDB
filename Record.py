from csv import reader

import Typee
import json


class Record:

    # constructor
    def __init__(self, type, entry, page_id):
        self.type = type
        self.entry = entry
        self.page_id = page_id

    # override equals
    def __eq__(self, other):
        return self.entry[1] == other.entry[1]


records = []  # all the records are in this list


def find_a_page_to_insert_record(type_name, pk):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    pass


def create_record(type_name, entry):
    typee = Typee.search_type(type_name)
    if type(typee) == int:
        return -1  # no such type
    if len(typee.fields) != len(entry):
        return -2  # fields does not match
    if [x for x in records if x.entry[1] == entry[1]] != []:
        return -3  # primary keys must be unique
    record = Record(type=type_name, entry=entry, page_id=-1)
    records.append(record)


def search_record(type_name, key):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    if type_name not in files_json.keys():
        return -1,-1,-1
    res = files_json[type_name]
    res.pop('fields', None)
    for file, pages in res.items():
        for page, intervals in pages.items():
            start = intervals['intervalStart']
            end = intervals['intervalEnd']
            if (int(start) >= int(key) >= int(end)) or (start == "" and end == ""):
                with open(f"./db/{type_name}/{file}/{page}.csv", "r") as page_csv:
                    records = reader(page_csv)
                    for record in records:
                        if record[1] == key:
                            return record,file,page
    return -2,-2,-2


def delete_record(typee, key):
    record,file,page = search_record(typee, key)
    if type(record) == int:
        return -1  # no such record
    else:
        records.remove(record)
        del record
        return 0


def update_record(typee, pkey, fields):
    if len(fields) == 0:
        return -1  # primary key cannot be null
    record,file,page = search_record(typee, pkey)
    if record == -1:
        return -1

    elif len(record) - 1 != len(fields):
        return -1  # field count does not match
    else:
        idx = records.index(record)
        records[idx].fields[1:] = fields
        records[idx].type = typee
        return 0


def list_all_records():
    return records


def filter_records(type_name, attribute, condition, number):
    """ actually we dont need this check since down below if list is empty, I return gracefully.
    type = Type.search_type(type_name)
    if type == -1:
        return ["type not found"]
    """
    temp_records = [x for x in records if attribute in x.entry.header]
    # proposal:
    temp_records = [x for x in records if attribute in Typee.get_headers(type_name)]

    if len(temp_records) == 0:
        return -1  # attribute does not exist probably
    attribute_index = temp_records[0].entry.index(attribute)
    if condition == "<":
        return [x for x in temp_records if x.entry[attribute_index] < number]
    elif condition == ">":
        return [x for x in temp_records if x.entry[attribute_index] > number]
    elif condition == "=":
        return [x for x in temp_records if x.entry[attribute_index] == number]
    else:
        pass
