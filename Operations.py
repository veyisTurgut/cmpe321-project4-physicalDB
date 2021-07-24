import Typee
import Record
import Filee
import Page
import json
import os
import shutil
from csv import reader
from csv import writer


######## Page Operations: object is a page ############


def addPageToAFile(type_name, file_id, page):
    # check whether file is full
    if not Filee.isFull(type_name, file_id):
        # if not full update files.json
        with open("./db/files.json", "r") as readfile:
            files_json = json.load(readfile)
        files_json[type_name]["file" + str(file_id)]["page" + str(page.id)] = {
            "intervalStart": "",
            "intervalEnd": "",
            "blankSpace": page.max_records
        }
        with open("./db/files.json", "w") as outfile:
            json.dump(files_json, outfile, indent=4)
    else:
        return -1


######## Type Operations: object is a type ############


def createNewType(type_name, number_of_fields, fields):
    # check constraints
    if len(type_name) > 19 or int(number_of_fields) > 9:
        return -1
    for field in fields:
        if len(field) > 19:
            return -2

    # add default fields
    fields = ['planet', 'id'] + fields

    # check if type already exists
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    if type_name in files_json.keys():
        return -3
        # create a file and a page
    file = Filee.create_file(type_name=type_name, fields=fields)
    page = Page.createPage(file_id=file.id, type_name=type_name, fields=fields)
    addPageToAFile(type_name, file.id, page)


def inheritType(target_type_name, source_type_name, fields):
    # check whether source type exists
    source = Typee.search_type(source_type_name)
    if source == -1:
        return -1
    inherited_fields = source['fields'][2:]
    fields = inherited_fields + fields
    # act as this is a new type creation with source fields - (planet & id fields) + additional fields
    return createNewType(target_type_name, len(fields), fields)


def listTypes():
    all_files = Filee.search_all_files()
    all_file_names = all_files.keys()
    return sorted(list(all_file_names)[1:])  # remove _comment field and sort 



######## Record Operations: object is a record ############

def readAPage(type_name, file_name, page_name):
    page_content = []
    # open the page in the file and read
    with open(f"./db/{type_name}/{file_name}/{page_name}.csv", "r") as page:
        for row in page:
            page_content.append(row)
    return page_content


def writeToPage(type_name, file_name, page_name, content):
    with open(f"./db/{type_name}/{file_name}/{page_name}.csv", "w") as page:
        page.write(''.join(content))


def recursiveInsertion(file_page_ids_list_for_insertion, row_number_to_insert, all_files, type_name, fields):
    #if fields[1] == "170":
    #    print(file_page_ids_list_for_insertion,row_number_to_insert)
    """
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    for file_page_id_comb in file_page_ids_list_for_insertion:
        if all_files[file_page_id_comb[0]][file_page_id_comb[1]]["blankSpace"] > 0:
            # just insert here, maybe? I dunno, I'm tired.
            page_content = readAPage(type_name, file_page_id_comb[0], file_page_id_comb[1])
            if row_number_to_insert == -1:
                page_content = [','.join(fields) + '\n'] + page_content[:]
            else:
                page_content = page_content[:row_number_to_insert] + [','.join(fields) + '\n'] + page_content[row_number_to_insert]
            writeToPage(
            type_name, file_page_id_comb[0], file_page_id_comb[1], page_content)

            interval_start = page_content[0][page_content[0].index(',') + 1:]
            interval_end = page_content[-1][page_content[-1].index(',') + 1:]
            files_json[type_name][str(file_page_id_comb[0])][str(file_page_id_comb[1])] = {
                "intervalStart": interval_start[:interval_start.index(',')],
                "intervalEnd": interval_end[:interval_end.index(',')],
                "blankSpace": files_json[type_name][file_page_id_comb[0]][file_page_id_comb[1]]["blankSpace"] - 1
            }
            with open("./db/files.json", "w") as outfile:
                json.dump(files_json, outfile, indent=4)

            return
    """
    #if all_files[file_page_id_comb[0]][file_page_id_comb[1]]["blankSpace"] == 0:
    if all_files[file_page_ids_list_for_insertion[-1][0]][file_page_ids_list_for_insertion[-1][1]]["blankSpace"] == 0:
            # create a new page
        if len(all_files[file_page_ids_list_for_insertion[-1][0]].keys())  < 8:
            page = Page.createPage(
                file_id=file_page_ids_list_for_insertion[-1][0][4:], type_name=type_name, fields=fields)
            addPageToAFile(
                type_name, file_page_ids_list_for_insertion[-1][0][4:], page)
        else:
            file = Filee.create_file(type_name=type_name, fields=fields)
            page = Page.createPage(
                file_id= file.id, type_name=type_name, fields=fields)
            addPageToAFile(type_name, file.id, page)
        file_page_ids_list_for_insertion.append(
            ["file" + str(page.file_id), "page" + str(page.id)])

    record_to_pass = ""
    # update json
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    for file_page_id_comb in file_page_ids_list_for_insertion:

        page_content = readAPage(
            type_name, file_page_id_comb[0], file_page_id_comb[1])

        if file_page_id_comb == file_page_ids_list_for_insertion[0]:  # first page is special, so we treat it specially
            record_to_pass = page_content[-1]
            if row_number_to_insert == -1:
                page_content = [','.join(fields) + '\n'] + page_content[:-1]
            else:
                page_content = page_content[:row_number_to_insert] + [
                    ','.join(fields) + '\n'] + page_content[row_number_to_insert:-1]
        # last page is also special
        elif file_page_id_comb == file_page_ids_list_for_insertion[-1]:
            page_content = [record_to_pass] + page_content
        else:
            temp = page_content[-1]
            page_content = [record_to_pass] + page_content[:-1]  # cut the last record
            record_to_pass = temp
        # write to csv
        writeToPage(
            type_name, file_page_id_comb[0], file_page_id_comb[1], page_content)
        interval_start = page_content[0][page_content[0].index(',') + 1:]
        interval_end = page_content[-1][page_content[-1].index(',') + 1:]
        files_json[type_name][str(file_page_id_comb[0])][str(file_page_id_comb[1])] = {
            "intervalStart": interval_start[:interval_start.index(',')],
            "intervalEnd": interval_end[:interval_end.index(',')],
            "blankSpace": files_json[type_name][str(file_page_id_comb[0])][str(file_page_id_comb[1])]["blankSpace"]
        }
    #print("143:", files_json[type_name][file_page_id_comb[0]][file_page_id_comb[1]])    
    files_json[type_name][str(file_page_id_comb[0])][str(file_page_id_comb[1])] = {
            "intervalStart": interval_start[:interval_start.index(',')],
            "intervalEnd": interval_end[:interval_end.index(',')],
            "blankSpace": files_json[type_name][file_page_id_comb[0]][file_page_id_comb[1]]["blankSpace"] - 1
        }

    with open("./db/files.json", "w") as outfile:
        json.dump(files_json, outfile, indent=4)


def createNewRecord(type_name, fields):  # fields[0] is id
    """algorithm: 
    precondition: we are given a record with its type
    steps:  1- check whether type exists. if yes, there must be at least a file and a page
            2- check whether record is valid
                2.1- lengths must be consistent with assumptions
                2.2- number of fields must match with type-fields
            3- find appropriate page to insert the record
                3.1- fetch all files
                3.2- check page intervals and find matching page, there are 4 cases. 
                    3.2.1- record key is greater than page1 start
                    3.2.2- record key is between a page
                    3.2.3- record key is between pages
                    3.2.4- record key is lesser than last page end
                    3.2.5- interval is empty which means this is the first record
                3.3- check whether PK already exists
            4- if page is full, hold last record of this page in a temp and insert this record. put that temp to a new page recursively.
            5- else which means page is nonnull, just insert and update intervals
    """
    # 1- check whether type exists
    if Typee.search_type(type_name) == -1:
        return -1  # type does not exists

    # 2.1- lengths must be consistent with assumptions
    for field in fields:
        if len(field) > 19:
            return -2

    fields = ['E226 − S187'] + fields
    all_files = Filee.search_files(type_name)

    # 2.2- number of fields must match with type-fields
    if len(fields) != len(all_files["fields"]):
        return -3
    # 3- find appropriate page to insert the record
    file_id_to_be_inserted, page_id_to_be_inserted = -1, -1
    is_found = False
    for file_name, file_content in all_files.items():
        # 3.1- fetch all files
        if file_name == "fields":
            continue
        # print("\t"+file_name,file_content)
        if is_found:
            break
        for page_id, page_content in file_content.items():
            """
            print("\t"*2+page_id, page_content)
            print(
                "\t"*3+fields[1], page_content['intervalStart'], page_content['intervalEnd'])
            """
            # 3.2.5- interval is empty which means this is the first record
            if page_content['intervalStart'] == "":
                #print("3.2.5")
                # which means page is brand new and this record is the first one since there is no interval
                file_id_to_be_inserted, page_id_to_be_inserted = 1, 1
                is_found = True
                break
            # 3.2.1- record :key is greater than page1 start
            if file_name == "file1" and page_id == "page1" and int(fields[1]) > int(page_content['intervalStart']):
                #print("3.2.1")
                file_id_to_be_inserted, page_id_to_be_inserted = 1, 1
                is_found = True
                break
            # 3.2.2- record key is in a page
            if int(fields[1]) <= int(page_content['intervalStart']) and int(fields[1]) >= int(page_content['intervalEnd']):
                #print("3.2.2")
                file_id_to_be_inserted, page_id_to_be_inserted = int(
                    file_name[4:]), int(page_id[4:])
                is_found = True
                break
            # 3.2.3- record key is between pages
            if int(fields[1]) > int(page_content['intervalStart']): # TODO : sth seems wrong intuitively. check it out. I think I should put +1 in if else block
                #print("3.2.3")
                if page_id == "page1":
                    file_id_to_be_inserted, page_id_to_be_inserted = int(
                        file_name[4:]), 1
                else:
                    file_id_to_be_inserted, page_id_to_be_inserted = int(
                        file_name[4:]), int(page_id[4:])
                is_found = True
                break

    # 3.2.4- record key is lesser than last page end
    # print(file_name,page_id)
    if file_id_to_be_inserted == -1 and page_id_to_be_inserted == -1:
        #print("3.2.4")
        file_id_to_be_inserted, page_id_to_be_inserted = int(
            file_name[4:]), int(page_id[4:])
    # print("fine until here")

    # 3.3- check whether PK already exists
    page_content = readAPage(
        type_name, "file" + str(file_id_to_be_inserted), "page" + str(page_id_to_be_inserted))
    line_count = 0
    row_number_to_insert = -1
    for row in page_content:
        row = row[row.index(',') + 1:]
        if row[:row.index(',')] == fields[1]:
            return -4  # PK key constraint failed
        if int(row[:row.index(',')]) > int(fields[1]):
            # print(row[:row.index(',')] > fields[1])
            row_number_to_insert = line_count + 1
        line_count += 1
    #print(row_number_to_insert)
    # 4- check whether page has space
    # if not
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    if files_json[type_name]["file"+str(file_id_to_be_inserted)]["page"+str(page_id_to_be_inserted)]["blankSpace"] == 0:
        """algo:
            we need to move the last record of this page to the next page. That page may be null.
            if null, create a page and insert this record
            if already exists. RECURSIVELY insert last record and move last record of that page
        """
        file_page_ids_list_for_insertion = []
        for file_name, file_content in all_files.items():
            if file_name == "fields" or int(file_name[4:]) < file_id_to_be_inserted:
                continue
            for page_name, page_info in file_content.items():
                if int(page_id[4:]) < page_id_to_be_inserted:
                    continue
                file_page_ids_list_for_insertion.append([file_name, page_name])
        #print("recursiveInsertion",file_page_ids_list_for_insertion,row_number_to_insert, all_files, type_name, fields)
        recursiveInsertion(file_page_ids_list_for_insertion,
                           row_number_to_insert, all_files, type_name, fields)

        """traverse pages until finding a nonfull page"""
        """while traversing, move last record of previous page to the beginning of current page"""
        """create a new file and a page if necessary"""
        # I already know which row to insert the record.

    # if yes
    # 5- else which means page is nonnull, just insert and update intervals
    else:
        if row_number_to_insert == -1:
            page_content = [','.join(fields) + '\n'] + page_content
            #print("295",page_content)
        else:
            i = 1
            for row in page_content:
                if i == row_number_to_insert:
                    page_content = page_content[:i] + \
                                   [','.join(fields) + '\n'] + page_content[i:]
                i = i + 1
        writeToPage(type_name, "file" + str(file_id_to_be_inserted),
                    "page" + str(page_id_to_be_inserted), page_content)
        """
        with open(f"./db/{type_name}/file{file_id_to_be_inserted}/page{page_id_to_be_inserted}.csv", "w") as page:
            page.write(''.join(page_content))
        """
        with open("./db/files.json", "r") as readfile:
            files_json = json.load(readfile)

        interval_start = page_content[0][page_content[0].index(',') + 1:]
        interval_end = page_content[-1][page_content[-1].index(',') + 1:]
        #print("349:", files_json[type_name]["file" + str(file_id_to_be_inserted)]["page" + str(page_id_to_be_inserted)]["blankSpace"])
        files_json[type_name]["file" + str(file_id_to_be_inserted)]["page" + str(page_id_to_be_inserted)] = {
            "intervalStart": interval_start[:interval_start.index(',')],
            "intervalEnd": interval_end[:interval_end.index(',')],
            "blankSpace":
                files_json[type_name]["file" + str(file_id_to_be_inserted)]["page" + str(page_id_to_be_inserted)][
                    "blankSpace"] - 1
        }
        with open("./db/files.json", "w") as outfile:
            json.dump(files_json, outfile, indent=4)


def filterType(type_name, attribute, operator, num):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)

    # check whether type exists
    if type_name not in files_json.keys():
        return -1
    # check whether attribute is valid.
    if attribute not in files_json[type_name]["fields"]:
        return -2
    attribute_idx = files_json[type_name]["fields"].index(attribute)
    record_list = []
    for file_name, file_content in files_json[type_name].items():
        # 3.1- fetch all files
        if file_name == "fields":
            continue
        for page_name in file_content.keys():
            for row in readAPage(type_name, file_name, page_name):
                target_field = row
                for i in range(attribute_idx):
                    target_field = target_field[target_field.index(',') + 1:]
                if "," in target_field:
                    target_field = target_field[:target_field.index(',')]
                if operator == "=":
                    operator = "=="
                if eval(str(target_field) + operator + str(num)):
                    record_list.append(row)
    return record_list

def searchRecord(type_name, pkey):
    #   print(Record.search_record(type_name, pkey))
    rec,file,page = Record.search_record(type_name, pkey)
    if rec == []:
        return -4,-4,-4
    return rec,file,page

def deleteRecord(type_name, pkey):
    # check whether type exists
    # if Typee.search_type(type_name) == -1:
    # delete record kitunian 9    return -1  # type does not exists

    is_present,file,page = searchRecord(type_name, pkey)
    if is_present is not None and type(is_present) == int and is_present < 0:
        return is_present

    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    # if type_name not in files_json.keys():
    #    return -2 

    res = files_json[type_name]
    fields = res.pop('fields', None)
    records_to_update = []
    line_to_delete = None
    page_to_update = None
    file_to_update = None
    leftover_count = 0
    for file, pages in res.items():
        for page, intervals in pages.items():
            start = intervals['intervalStart']
            end = intervals['intervalEnd']
            records_to_update = []
            if (int(start) >= int(pkey) >= int(end)) or (start == "" and end == ""):
                with open(f"./db/{type_name}/{file}/{page}.csv", "r", newline='', encoding="utf-8") as page_csv:
                    records = reader(page_csv)
                    for line, record in enumerate(records):
                        records_to_update.append(record)
                        if record[1] == pkey:  # row to delete is found
                            line_to_delete = line
                            page_to_update = page
                            file_to_update = file
                    if line_to_delete is not None:
                        page_csv.close()
                        break
    if page_to_update is None:
        return -3
    else:
        page_content = readAPage(type_name,file_to_update,page_to_update)
        page_content.remove(page_content[line_to_delete])
        writeToPage(type_name,file_to_update,page_to_update,page_content)
        leftover_count = len(page_content)

    if leftover_count > 0:
        interval_start = page_content[0][page_content[0].index(',') + 1:]
        interval_end = page_content[-1][page_content[-1].index(',') + 1:]
        files_json[type_name]["fields"] = fields
        files_json[type_name][file_to_update][page_to_update] = {
                "intervalStart": interval_start[:interval_start.index(',')],
                "intervalEnd": interval_end[:interval_end.index(',')],
                "blankSpace":
                    files_json[type_name][file_to_update][page_to_update]["blankSpace"] + 1
            }
        with open("./db/files.json", "w") as outfile:
            json.dump(files_json, outfile, indent=4)


    files_json[type_name]["fields"] = fields  # Replace fields we want to write them back
    # if the page is empty, delete the page
    if leftover_count == 0:
        os.remove(f"./db/{type_name}/{file_to_update}/{page_to_update}.csv")
        del files_json[type_name][file_to_update][page_to_update]
        with open("./db/files.json", "w") as outfile:
            json.dump(files_json, outfile, indent=4)

    # if the file is empty and there are more than 1 file of that type, delete the file
    if len(files_json[type_name][file_to_update]) == 0 and len(
            files_json[type_name].keys()) > 2:  # Also counting "fields" key
        shutil.rmtree(f"./db/{type_name}/{file_to_update}")
        del files_json[type_name][file_to_update]
        with open("./db/files.json", "w") as outfile:
            json.dump(files_json, outfile, indent=4)


def listRecords(type_name):
    # check whether type exists
    if Typee.search_type(type_name) == -1:
        return -1  # type does not exists
    output = ""
    record_type = Typee.search_type(type_name)
    fields = record_type.pop('fields', None)  # remove the fields key
    for record_file in list(record_type.keys()):
        for record_page in list(record_type[record_file].keys()):
            with open(f"./db/{type_name}/{record_file}/{record_page}.csv", "r", encoding="utf-8") as page_csv:
                records = reader(page_csv)
                for record in records:
                    output += ",".join(record)
                    output += "\n"
                page_csv.close()
    # if output is empty return failure
    if output == "":
        return -2
    return output


def updateRecord(type_name, pkey, fields):
    # check whether type exists
    if Typee.search_type(type_name) == -1:
        return -1  # type does not exists

    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)
    if type_name not in files_json.keys():
        return -2
    res = files_json[type_name]
    res.pop('fields', None)
    records_to_update = []
    line_to_update = None
    page_to_update = None
    file_to_update = None
    for file, pages in res.items():
        for page, intervals in pages.items():
            start = intervals['intervalStart']
            end = intervals['intervalEnd']
            records_to_update = []
            if (int(start) >= int(pkey) >= int(end)) or (start == "" and end == ""):
                with open(f"./db/{type_name}/{file}/{page}.csv", "r", newline='', encoding="utf-8") as page_csv:
                    records = reader(page_csv)
                    for line, record in enumerate(records):
                        records_to_update.append(record)
                        if record[1] == pkey:  # row to update is found
                            line_to_update = line
                            page_to_update = page
                            file_to_update = file
                    if line_to_update is not None:
                        page_csv.close()
                        break
    if page_to_update is None:
        return -1
    else:
        with open(f"./db/{type_name}/{file_to_update}/{page_to_update}.csv", "w", newline='',
                  encoding="utf-8") as write_obj:
            new_csv = writer(write_obj)
            for line, row in enumerate(records_to_update):
                if line == line_to_update:
                    new_csv.writerow(['E226 - S187', pkey] + fields)
                else:
                    new_csv.writerow(row)
            write_obj.close()


# todo: create physical csv file
# TODO: I already wrote createNewType above. :///
def createType(type_name, fields):
    if len(type_name) > 19 or len(fields) > 9:
        return -1

    for field in fields:
        if len(field) > 19:
            return -1

    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)

    if type_name in files_json:
        return -1

    os.mkdir("./db/" + type_name)
    os.mkdir("./db/" + type_name + "/file1")
    # Create type object
    type = {}
    type["fields"] = fields
    type["file1"] = {}
    files_json[type_name] = type

    with open("./db/files.json", "w") as outfile:
        json.dump(files_json, outfile, indent=4)


def deleteType(type_name):
    with open("./db/files.json", "r") as readfile:
        files_json = json.load(readfile)

    if type_name not in files_json:
        return -1

    shutil.rmtree("./db/" + type_name)

    # Delete type object
    del files_json[type_name]

    with open("./db/files.json", "w") as outfile:
        json.dump(files_json, outfile, indent=4)


