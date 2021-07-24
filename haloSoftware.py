import csv
import sys
import time
import Operations


def main():
    # get command line arguments
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    # input operations
    infile = open(arg1, 'r')
    lines = infile.read().splitlines()
    lines = [line.strip() for line in lines]
    # output operations
    outfile = open(arg2, "w")
    logfile = open('haloLog.csv', 'a')
    # log operations
    log_writer = csv.writer(logfile)
    log_writer.writerow(['username', 'occurrence', 'operation', 'status'])

    for line in lines:
        res = 0
        keywords = line.lower().split()
        """
        if keywords[0] == 'register':  # Authentication Language Operations -> register
            username = keywords[2]
            password = keywords[3]
            password_repeat = keywords[4]

        elif keywords[0] == 'login':  # Authentication Language Operations -> login
            username = keywords[1]
            password = keywords[2]

        elif keywords[0] == 'logout':  # Authentication Language Operations -> logout
            pass 
        """
        # Definition Language Operations -> create
        if keywords[0] == 'create' and keywords[1] == 'type':
            if len(keywords) < 4:
                res = -1
            else:
                type_name = keywords[2]
                number_of_fields = int(keywords[3])
                fields = keywords[4:]
                res = Operations.createNewType(type_name, number_of_fields, fields)

        # Definition Language Operations -> delete
        elif keywords[0] == 'delete' and keywords[1] == 'type':
            type_name = keywords[2]
            res = Operations.deleteType(type_name)

        # Definition Language Operations -> inherit
        elif keywords[0] == 'inherit' and keywords[1] == 'type':
            target_type_name = keywords[2]
            source_type_name = keywords[3]
            fields = keywords[4:]
            res = Operations.inheritType(target_type_name, source_type_name, fields)

        # Definition Language Operations -> list
        elif keywords[0] == 'list' and keywords[1] == 'type':
            res = Operations.listTypes()
            if type(res) == list:
                outfile.write('\n'.join(res))
                outfile.write('\n')
                res = 0

        # Management Language Operations -> create
        elif keywords[0] == 'create' and keywords[1] == 'record':
            type_name = keywords[2]
            fields = keywords[3:]
            res = Operations.createNewRecord(type_name, fields)

        # Management Language Operations -> delete
        elif keywords[0] == 'delete' and keywords[1] == 'record':
            type_name = keywords[2]
            pkey = keywords[3]
            res = Operations.deleteRecord(type_name, pkey)

        # Management Language Operations -> update
        elif keywords[0] == 'update' and keywords[1] == 'record':
            type_name = keywords[2]
            pkey = keywords[3]
            fields = keywords[4:]
            res = Operations.updateRecord(type_name, pkey, fields)

        # Management Language Operations -> search
        elif keywords[0] == 'search' and keywords[1] == 'record':
            type_name = keywords[2]
            pkey = keywords[3]
            res = Operations.searchRecord(type_name, pkey)
            if type(res) != int:
                if len(res) == 1:
                    outfile.write(res[0])
                res = 0

        # Management Language Operations -> list
        elif keywords[0] == 'list' and keywords[1] == 'record':
            type_name = keywords[2]
            res = Operations.listRecords(type_name)
            if type(res) != int:
                outfile.write(res)
                res = 0

        # Management Language Operations -> filter
        elif keywords[0] == 'filter' and keywords[1] == 'record':
            type_name = keywords[2]
            condition = keywords[3]
            ind = max(condition.find('<'), condition.find(
                '>'), condition.find('='))
            operator = condition[ind]
            attribute = condition[:ind]
            num = int(condition[ind + 1:])
            outfile.write(''.join(Operations.filterType(type_name, attribute, operator, num)))

        if res is not None and res < 0:
            status = 'failure'
        else:
            status = 'success'

        log_writer.writerow(['admin', str(int(time.time())), str(line), status])

    infile.close()
    outfile.close()
    logfile.close()


if __name__ == '__main__':
    main()
