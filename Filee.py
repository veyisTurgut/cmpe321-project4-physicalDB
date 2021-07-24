import json


class Filee:

    # constructor
    def __init__(self, type_name, fields):
        with open("./db/files.json", "r") as readfile:
            files_json = json.load(readfile)
        if type_name in files_json.keys():
            self.id = len(files_json[type_name])
        else:
            self.id = 1
        self.size = 3192 * 8
        self.pageList = []
        self.type_name = type_name

        # update files.json
        if self.id == 1:
            files_json[type_name] = {
                "fields": fields,
                "file1": {}
            }
        else:
            files_json[type_name]["file" + str(self.id)] = {}
        with open("./db/files.json", "w") as outfile:
            json.dump(files_json, outfile, indent=4)
        # create folder of the file.

    # override toString()
    def __str__(self):
        return f"id: {self.id}, type:{self.type_name}"

    def readPage(self, page_id):
        """ with open("./db/files.json", "r") as readfile:
            files_json = json.load(readfile)
            pages = files_json[self.type_name]["file-"+self.id][page_id]
        return pages
        # or """
        with open(f"./db/{self.type_name}/file{self.id}/page{page_id}.csv", "r") as page:
            pass

    def addPage(self, page):
        # check whether file is full
        if not self.isFull():
            # self.pageList.append(page)
            # update files.json
            with open("./db/files.json", "r") as readfile:
                files_json = json.load(readfile)
            files_json[self.type_name]["file" + str(self.id)]["page" + str(page.id)] = {
                "intervalStart": "Z",
                "intervalEnd": "0"
            }
            with open("./db/files.json", "w") as outfile:
                json.dump(files_json, outfile, indent=4)
        else:
            return -1

    def deletePage(self, page):
        # there should remain at least one page
        if not len(self.pageList) == 1:
            ind = self.pageList.index(page)
            self.pageList.pop(ind)
        else:
            pass

    def isFull(self):
        return len(self.pageList) == 8


files = []


def get_file(file_id):
    file = [x for x in files if x.id == files]
    return -1 if len(file) == 0 else file[0]


# we can either return file names, files with their pages as a dict but returning Filee object doesn't seem fine to me.
def search_files(type_name):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    return files_json[type_name]
    # or
    # return files_json[type_name].keys()
    # below doesn't seem right
    # return [x for x in files if x.type_name == type_name]


def search_all_files():
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    return files_json


def delete_file(file):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    files_json.pop(file.type)
    del file
    pass


def create_file(type_name, fields):
    return Filee(type_name, fields)


def isFull(type_name, file_id):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
        try:
            return len(files_json[type_name]["file" + str(file_id)]) == 8
        except Exception as e:
            print(e,"file_is_full\n")
