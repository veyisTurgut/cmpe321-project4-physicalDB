# cmpe321-p4

<br><br>
- **CMPE 321, Introduction to Database Systems**
- Spring 2021
- Adalet Veyis Turgut 
- Ufuk Arslan 
- Zuhal Didem Aytaç 


<br><br>
***Assumptions & Constraints***<br>

- Maximum length of a field name = 19 characters
- Maximum length of a field value = 19 characters
- Size of a field = fixed 19 bytes
- Maximum number of fields in a type = 10 (including Planet)
- Size of a type = (number of fields) * (size of a field) = (number of fields) * 19
- Size of a page = fixed 3192 bytes
- Maximum number of records in a page = 3192 // (size of the type the page contains)
- Size of a file = 3192 * 8 Bytes
- Maximum number of pages in a file = 8

<br><br>
***Storage Structures***<br>
Explain your system catalog, page design, page header, record header, etc. with tables/diagrams/figures.

- Types
  - Types are stored inside the `files.json` file. Each object key of `files.json` is the name of a specific type. Inside each type we store related files as json objects.

- Files
  - Files are stored inside the `files.json` file under their corresponding types. Each file object contains an array of page informations. Those informations consits of the page id (pointer to the page), start and the end of the interval of the primary keys inside that page. We store the end and start intervals to make seaching and sorting faster.

- Pages
  - Pages are `.csv` files stored inside folders named as `file<file-id>`, and those file folders are stored inside the folders named as `type<type-id>`. So, each page of the same type are stored together inside multiple folders. Page keys inside `files.json` file works as page headers as we can reach any page data from any type and file.

- Records
  - A record is basically a row inside `page<page-id>.csv` file. The fields of a record is given in the header of the corresponding `.csv` file. Start and end intervals of primary keys of records inside `files.json` file works as record headers as we can reach any record from any type, file, and page.

Here is an example `files.json` file:
```yaml
{
    "_comment": "first keys are type names. Type names are unique. Types has files, so inner keys are filenames. They have suffixes like -1,-2. Finally files have pages.",
    "animal": {
        "fields": [
            "planet",
            "id",
            "name",
            "age",
            "height",
            "weight"
        ],
        "file1": {
            "page1": {
                "intervalStart": "",
                "intervalEnd": "",
                "blankSpace": 28
            }
        }
    },
    "human": {
        "fields": [
            "planet",
            "id",
            "name",
            "age",
            "height",
            "weight",
            "alias",
            "occupation"
        ],
        "file1": {
            "page1": {
                "intervalStart": "3",
                "intervalEnd": "1",
                "blankSpace": 18
            }
        }
    },
    "kitunian": {
        "fields": [
            "planet",
            "id",
            "name",
            "age",
            "height",
            "weight",
            "color",
            "fangcount"
        ],
        "file1": {
            "page1": {
                "intervalStart": "11",
                "intervalEnd": "1",
                "blankSpace": 16
            }
        }
    }
}
```
  
<br><br>
***Operations***<br>

<br>
- HALO Definition Language Operations
  - Create
    - Creates a new type with given name that has the given fields.
    - Input format : create type <type-name><number-of-fields><field1-name><field2-name>...  
    - Output format : None
    - The type name can be at most 19 characters long.
    - The number of fields can be at most 9 (with default field Planet it can be at most 10).
    - The field names can be at most 19 characters long.
    - A page for the new type is created.
  - Delete
    - Deletes the given type and its records from the system.
    - Input format : delete type <type-name>
    - Output format : None
    - The type should exist in the system
    - The pages and files of the given type is deleted. 
  - Inhterit
    - Creates a new type with given target name that has the given fields and the fields of the source type.
    - Input format : inherit type <target-type-name> <source-type-name> <additional-field1><additional-field2>...
    - Output format : None
    - The source type should exist in the system
    - Follows the same procedure with Create Type; type-name being target type name, the fields being the additional fields + the fields of source type
  - List
    - Lists the names of all types.
    - Input format : list type
    - Output format : <type1-name> <type2-name> ...
  
- HALO Management Language Operations
  - Create
    - Creates a record of the given type with the given field values.
    - Input format : create record <type-name><field1-value><field2-value>...
    - Output format : None
    - The type should exist in the system.
    - The number of fields should match with the number of fields of the type.
    - The field values can be at most 19 characters long.
  - Delete
    - Deletes the given record from the system.
    - Input format : delete record <type-name><primary-key>
    - Output format : None
    - The type should exist in the system.
    - There should exist a record of the given type with the given primary key.
    - The record is deleted from the page it appears. If the page is empty after the delete the page is also deleted, assuring that there exist at least one page in the corresponding file.
  - Update
    - Updates the given record's fields with the given values.
    - Input format : update record <type-name><primary-key><field2-value><field3-value>...
    - Output format : None
    - The type should exist in the system.
    - There should exist a record of the given type with the given primary key.
    - The number of fields of the type should match with the given field values.
    - The field values except the value for field Planet are updated.
  - Search
    - Returns the field values of the given record.
    - Input format : search record <type-name><primary-key>
    - Output format : <field1-value><field2-value>...
    - The type should exist in the system.
    - There should exist a record of the given type with the given primary key.
  - List
    - Lists the field values of all records of the given type.
    - Input format : list record <type-name>
    - Output format : <record1-field1-value><record1-field2-value>... <record2-field1-value><record2-field2-value>... ...
    - The type should exist in the system.
  - Filter
    - Lists the field values of all records of the given type that satisfy the given condition.
    - Input format : filter record <type-name><condition>
    - Output format : <record1-field1-value><record1-field2-value>... <record2-field1-value><record2-field2-value>... ...
      
