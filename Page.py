import Record
import Typee
import json
import os


class Page:

    # constructor
    def __init__(self, type_name, file_id, fields):
        with open("./db/files.json", "r") as readfile:
            files_json = json.load(readfile)
        self.id = (int(list(files_json[type_name]["file"+str(file_id)].keys())[-1][4:]) + 1) if (len(files_json[type_name]["file"+str(file_id)].keys()) > 0) else 1
        self.size = 3192
        self.file_id = file_id
        self.fields = fields
        self.recordList = []
        self.type_name = type_name
        self.max_records = 3192 // (19 *
                                    len(Typee.search_type(type_name)["fields"]))

        # create physical csv file
        if file_id == 1:
            try:
                os.mkdir(f"./db/{self.type_name}")
            except Exception as e:
                print(e, "at page, create type folder failed")
                pass
        if self.id == 1:
            try:
                os.mkdir(f"./db/{self.type_name}/file{self.file_id}")
            except Exception as e:
                print(e, "at page, create file folder failed")
                pass
        with open(os.path.join(f"./db/{self.type_name}/file{self.file_id}", f"page{self.id}.csv"), 'w') as fp:
            pass

    def addRecord(self, record: Record):
        if self.type_name == record.type:
            self.recordList.append(record)
        else:
            return -1

    def searchRecord(self, record):
        if self.type_name != record.type:
            return -1
        else:
            pass

    def listAllRecords(self, record):
        if self.type_name != record.type:
            return -1
        else:
            pass

    def isFull(self):
        return len(pages) == self.max_records


pages = []  # all the pages are in this list


def searchPage(type_name):
    pages_with_this_type = [x for x in pages if x.type_name == type_name]
    return pages_with_this_type
    # return type_name in


def createPage(type_name, file_id, fields):
    return Page(type_name, file_id, fields)


def get_page(page_id):
    page = [x for x in pages if x.id == page_id]
    return -1 if len(page) == 0 else page[0]


def deletePage(page_id):
    page = get_page(page_id)
    pages.remove(page)
    del page
    return 0
