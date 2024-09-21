# Import regex, used for the validation functions
import re

#
# DATABASE AND TABLES
#

# The Table class, which contains all the manipulating of the database structure
# It contains the creating, deleting, and amending of records, where the data in the text file is encrypted

class Table():

    # Contains the 'metadata' for the information (a multidimensional array) in the database,
    # such as the name of the table itself, and the fields that the information is related to.

    # It also contains the properties of each field, starting from the left to right:
    # ["Is it a foreign key, a primary key, or neither?",
    # "The type of the field",
    # "The max length of the field",
    # "The default value of field",
    # "Any additional format checks",
    # "And is it required?"]

    # These are for each table
    enumOfTableData = {
        0: {"name": "Staff Details",
            "fields": [
                       ["staffID", ["P", int, "", "", "", True]],
                       ["staffFirstName", ["", str, 30, "", ["format", "name"], True]],
                       ["staffLastName", ["", str, 30, "", ["format", "name"], True]],
                       ["telephoneNum", ["", str, 11, "", ["format", "phone"], True]],
                       ["emailAddress", ["", str, 30, "", ["format", "email"], True]],
                       ["homeAddress", ["", str, 50, "", ["format", "address"], True]],
                       ["position", ["", str, 20, "", ["format", "position"], True]],
                       ["workingHours", ["", int, 3, "", ["range", 168], True]],
                       ["salary", ["", int, 5, "", ["range", 99999], True]]
            ]},
        1: {"name": "Account Details",
            "fields": [
                       ["accountID", ["P", int, "", "", "", True]],
                       ["staffID", ["F", int, "", "", "", True]],
                       ["username", ["", str, 30, "", "", True]],
                       ["password", ["", str, 20, "Password", "", True]]
            ]},
        2: {"name": "Computer Reservations",
            "fields": [
                       ["computerReservationID", ["P", int, "", "", "", True]],
                       ["customerID", ["F", int, "", "", "", True]],
                       ["computerID", ["F", int, "", "", "", True]],
                       ["dateOfUse", ["", str, 8, "", ["format", "date"], True]],
                       ["timeOfUseStart", ["", str, 5, "", ["format", "time"], True]],
                       ["timeOfUseEnd", ["", str, 5, "", ["format", "time"], True]],
                       ["amountOfTime", ["", float, 4, "", ["range", 9999], True]],
                       ["boolFinished", ["", bool, 1, 0, "", True]]
            ]},
        3: {"name": "Computer Status",
            "fields": [
                       ["computerID", ["P", int, "", "", "", True]],
                       ["boolOperable", ["", bool, 1, 0, "", True]],
                       ["boolMalware", ["", bool, 1, 0, "", True]],
                       ["boolFullDrive", ["", bool, 1, 0, "", True]],
                       ["comments", ["", str, 200, "", "", False]],
                       ["date", ["", str, 8, "", ["format", "date"], True]]
            ]},
        4: {"name": "Repair Reservations",
            "fields": [
                       ["repairReservationID", ["P", int, "", "", "", True]],
                       ["customerID", ["F", int, "", "", "", True]],
                       ["dateOfReservation", ["", str, 8, "", ["format", "date"], True]],
                       ["timeOfReservationStart", ["", str, 5, "", ["format", "time"], True]],
                       ["timeOfReservationEnd", ["", str, 5, "", ["format", "time"], True]],
                       ["device", ["", str, 40, "", "", True]],
                       ["problems", ["", str, 100, "", "", True]],
                       ["estimatedTimeToFix", ["", float, 3, "", ["range", 999], True]],
                       ["boolFinished", ["", bool, 1, 0, "", True]]
            ]},
        5: {"name": "Stocks",
            "fields": [
                       ["stockID", ["P", int, "", "", "", True]],
                       ["stockName", ["", str, 20, "", "", True]],
                       ["stockValue", ["", int, 4, 0, ["range", 9999], True]],
                       ["warningValue", ["", int, 4, 0, ["range", 9999], True]],
                       ["date", ["", str, 8, "", ["format", "date"], True]],
                       ["approximateTime", ["", str, 5, "", ["format", "time"], True]],
                       ["comments", ["", str, 200, "", "", False]]
            ]},
        6: {"name": "Customer Details",
            "fields": [
                       ["customerID", ["P", int, "", "", "", True]],
                       ["firstName", ["", str, 30, "", ["format", "name"], True]],
                       ["lastName", ["", str, 30, "", ["format", "name"], True]],
                       ["telephoneNum", ["", str, 11, "", ["format", "phone"], False]],
                       ["emailAddress", ["", str, 30, "", ["format", "email"], False]],
                       ["points", ["", int, 5, 0, ["range", 99999], True]]
            ]},
        7: {"name": "Transaction History",
            "fields": [
                       ["transactionID", ["P", int, "", "", "", True]],
                       ["stockID", ["F", int, "", "", "", True]],
                       ["accountID", ["F", int, "", "", "", True]],
                       ["change", ["", str, 200, "", "", True]]
            ]}
    }

    # Instantiates the table, saving the table's id, name, fields, and unique identifier
    def __init__(self, tableIdentifier):

        # If the tableIdentifier is a string, treat it as the name of the table, rather than its enum ID
        if (type(tableIdentifier) is str):

            # Linearly search through enumOfTableData dictionary and compare the name of the table to the tableIdentifier
            for id, data in Table.enumOfTableData.items():

                # The table number is found
                if data["name"] == tableIdentifier:
                    self.tableNum = id
        else:
            # If the tableIdentifier is not a string, then the tableIdentifier is the tableID in the enum,
            # therefore, assign it to self.tableNum
            self.tableNum = tableIdentifier


        # Gets the table's name from the data, based on the id passed in
        self.tableName = self.enumOfTableData[self.tableNum]['name']

        # Gets the field data, which contains their properties
        self.tableFieldData = self.enumOfTableData[self.tableNum]['fields']

        # Creates a list for each of the field names
        self.tableFields = [x[0] for x in self.enumOfTableData[self.tableNum]['fields']]

        # In the sequential text file database, the table identifier serves as a header for where to and from the table
        # should read to gather their respective records.
        self.tableIdentifier = f"#~{self.tableNum}"

        # This checks for if the database file exists in the directory, if not, create one, and finally close the file
        try:
            file = open("db.txt")
        except:
            file = open("db.txt", "w")
        finally:
            file.close()

    # This method reads the records concerning its own table and converts it to a list for manipulation in other methods
    # This method is private as indicated by the two underscores
    def __tableToList(self):

        # Open the database in readonly format
        with open("db.txt", "r") as file:

            # Decrypts the database and converts it into a list of records
            file = [self.__decryption(file.read())][0].split("\n")

            # If the file is empty, make the file list empty
            file = [] if file == [""] else file

            # List to store the records
            recordsList = []

            # Linearly searches from the first line and ignores the data until it recognises its own unique identifier
            tableFlag = False
            for databaseLine in file:
                if (tableFlag):
                    if ("#~" in databaseLine):
                        break
                    else:
                        # A single record which is decrypted
                        record = databaseLine.split(",")

                        # Adds decrypted record to list
                        recordsList.append(record)

                if (self.tableIdentifier in databaseLine):
                    tableFlag = True

        # Results in a decrypted list ready for usage elsewhere
        return recordsList

    # This method prints out the table onto the console
    def listToViewable(self):

        # Get decrypted list of records
        recordsList = self.__tableToList()

        # Starts at -1 to put in the fields first
        for record in range(-1, len(recordsList)):
            if (record == -1):
                # Prints fields
                print(" ".join(self.tableFields))

                # If there are no records in the table, print that there are none
                if (len(recordsList) == 0):
                    print("No Records (0)")
            else:
                # Prints the decrypted record
                print(" ".join(recordsList[record]))

    # This method gets the number of records in a table
    def tableLength(self):

        # Get decrypted list of records
        records = self.__tableToList()

        # Return the length of the list
        return len(records)

    # Private method that gets to the highest primary key ID in a table
    def __getHighestID(self):

        # Get decrypted list of records
        records = self.__tableToList()
        # Iterates through the table and compares until it gets the highest ID
        highestID = -1
        for record in records:
            if (int(record[0]) > highestID):
                highestID = int(record[0])

        return highestID

    # Creates a record
    def createRecord(self, fields):

        # If the number of attributes given are not equal to the fields, it is invalid
        if (len(fields) != len(self.tableFields)-1):
            return print("Invalid number of fields.")

        # Gets the highest ID in the table
        ID = str(self.__getHighestID()+1 if self.__getHighestID() != -1 else 0)

        # Makes the record
        createdRecord = f"{ID}," + ",".join(fields)

        # Opens the database
        with open("db.txt", "r") as file:
            decryptedDatabase = self.__decryption(file.read())
            databaseRecords = decryptedDatabase.split("\n")

        # If the file is empty, make the file list empty
        databaseRecords = [] if databaseRecords == [""] else databaseRecords

        # This is used to find if the table has an identifier in the database
        checkForIdentifier = True

        # Used to store every record in the database
        databaseRecordsList = []

        # This simply finds the table's unique identifier and inserts the record below it (linear search)
        for line in databaseRecords:
            databaseRecordsList.append(line)
            if (self.tableIdentifier in line):
                databaseRecordsList.append(createdRecord)
                checkForIdentifier = False

        # If an identifier wasn't found, make one at the end of the file and add the record
        if (checkForIdentifier):
            databaseRecordsList.append(self.tableIdentifier)
            databaseRecordsList.append(createdRecord)

        # Converts the list into a string with newlines
        databaseRecordsPlain = "\n".join(databaseRecordsList)

        # Write the whole list into the database
        with open("db.txt", "w") as file:
            file.write(self.__encryption(databaseRecordsPlain))

    # This method deletes a record in the table by using its index
    def deleteRecord(self, index):

        # If index is greater than the table size or its negative, raise error
        if (index > len(self.__tableToList())-1 or index < 0):
            return print("Failed to delete, index out of bounds. Index likely bigger than list size.")

        # This searches through the whole database
        databaseRecordsList = []
        with open("db.txt", "r") as file:
            file = self.__decryption(file.read()).split("\n")

        # If the file is empty, make the file list empty
        file = [] if file == [""] else file

        # The counter is used to find the start of the table in the database (linear search)
        indexCounter = 0
        for preTable in file:
                databaseRecordsList.append(preTable)
                indexCounter += 1

                # If the line contains the table identifier i.e the start of the table, then break
                if (self.tableIdentifier in preTable):
                    break

        # The counter is used to find the index of the records (linear search)
        counter = 0
        for tableLine in file[indexCounter:]:
            # If the record with the specified index is found, it is not added to the new database, effectively removing it
            if (counter != index):
                databaseRecordsList.append(tableLine)
            counter += 1

        # Converts the list into a string with newlines
        databaseRecordsPlain = "\n".join(databaseRecordsList)

        # Write the whole list into the database
        with open("db.txt", "w") as file:
            file.write(self.__encryption(databaseRecordsPlain))

    # This method amends a record
    def amendRecord(self, index, field, value):

        # If index is greater than the table size or its negative, raise error
        if (index > len(self.__tableToList())-1 or index < 0):
            return print("Failed to delete, index out of bounds. Index likely bigger than list size.")

        # Gets the relevant information by the user input
        amendedRecord = self.__getRecordByIndex(index)
        fieldIndex = self.tableFields.index(field)
        amendedRecord[fieldIndex] = value

        # Formats record
        amendedRecord = [field for field in amendedRecord]
        amendedRecord = ",".join(amendedRecord)

        # This does a mix of both the createRecord and deleteRecord methods, it deletes the old record
        # and replaces it with the new one by finding its index
        # This searches through the whole database
        databaseRecordsList = []
        with open("db.txt", "r") as file:
            file = self.__decryption(file.read()).split("\n")

        # If the file is empty, make the file list empty
        file = [] if file == [""] else file

        # The counter is used to find the start of the table in the database (linear search)
        indexCounter = 0
        for preTable in file:
            databaseRecordsList.append(preTable)
            indexCounter += 1

            # If the line contains the table identifier i.e the start of the table, then break
            if (self.tableIdentifier in preTable):
                break

        # The counter is used to find the index of the records (linear search)
        counter = 0
        for tableLine in file[indexCounter:]:
            # If the record with the specified index is found, it is not added to the new database, and instead the new record is added
            if (counter != index):
                databaseRecordsList.append(tableLine)
            else:
                databaseRecordsList.append(amendedRecord)
            counter += 1

        # Converts the list into a string with newlines
        databaseRecordsPlain = "\n".join(databaseRecordsList)

        # Write the whole list into the database
        with open("db.txt", "w") as file:
            file.write(self.__encryption(databaseRecordsPlain))

    # This method checks to see if a record exists based on a searchValue
    def verifyRecordExistence(self, searchValue, index=0):

        # Get decrypted list of records
        records = self.__tableToList()

        # Linearly search through the records and if found, return true
        for record in records:
            if (record[index] == searchValue):
                return True

        # If it cannot be found, therefore return false
        return False

    # This method gets a record by its index
    def __getRecordByIndex(self, index):

        # Get decrypted list of records
        records = self.__tableToList()

        # If index is greater than the table size or its negative, raise error
        if (index > len(records) - 1 or index < 0):
            return print("Failed to find, index out of bounds. Index likely bigger than list size.")

        return records[index]

    # This method finds a record by a search value (NOT an index, like the __getRecordByIndex method), using
    # a sorting and a searching algorithm
    def findRecord(self, field, searchValue):

        # Gets decrypted list of records
        records = self.__tableToList()

        # Uses the field to find the index of the field in the fields list
        fieldIndex = self.tableFields.index(field)

        # This uses bubble sort to sort by a field
        records = self.__bubbleSort(records, fieldIndex)

        # This uses a binary search to find a record by its field and search value
        record = self.__binarySearch(records, fieldIndex, searchValue)

        return record

    # This method sorts records by bubble sort
    def __bubbleSort(self, records, sortValue):

        # Loops for the number of records in records
        for record in range(len(records)):

            # Loops for the remaining number of records to sort (the records that are not in the correct place)
            for remaining in range(0, len(records)-(record+1)):

                # If the current record's field is greater than the next record's field, swap their values
                if (records[remaining][sortValue] > records[remaining + 1][sortValue]):
                    records[remaining], records[remaining + 1] = records[remaining + 1], records[remaining]

        return records

    # This method searches for a record by binary search
    def __binarySearch(self, records, field, searchValue):

        # Low is the lowest index value, high is the highest index value of the records
        low, high = 0, len(records)-1

        # Loops as long the boundaries don't overlap or cross over
        while low <= high:

            # Gets the midpoint between the high and low boundaries
            mid = low + (high - low)//2

            # Converts the field in record's type to the searchValue's type, then compares with the search value
            # If equal, return the record
            if (type(searchValue)(records[mid][field]) == searchValue):
                return records[mid]

            # Otherwise, shift the boundaries to half the records from the midpoint based on whether the record is
            # on the lower end or the higher end
            elif (type(searchValue)(records[mid][field]) < searchValue):
                low = mid + 1
            else:
                high = mid - 1

        # If the record is not found, return -1
        return -1


    # This method encrypts plain text to cipher text
    def __encryption(self, plain):
        # This represents the list of each character the encryption can convert to the cipher text
        characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 /:@.,#~\n'")

        # The key is the variable that changes how the resultant cipher is made. The larger the value and variance in
        # characters, the more secure it is
        key = list("T3OeM2aIXsDJp4LwPAgY")
        cipherCharacters = []

        # This variable keeps track of how far the encryption is in the key. If it reaches the end of the key,
        # it loops back to the first character
        keyCharCounter = 0
        for character in plain:
            # The index of the character, plus the index of key in relation to the characters list, modulus
            # by the number of characters in the characters list, equals the new cipher character
            characterNum = (characters.index(character) + characters.index(key[keyCharCounter])) % len(characters)
            cipherCharacter = characters[characterNum]
            cipherCharacters.append(cipherCharacter)

            # Checks for whether the characters in the key has 'ran out', if so, loop back to the first character
            keyCharCounter += 1
            if (keyCharCounter > len(key)-1):
                keyCharCounter = 0

        # Returns the ciphered text
        return "".join(cipherCharacters)

    # This method is nearly identical to the encryption method, except it has a minus instead of a plus
    # when determining cipher character
    def __decryption(self, cipher):
        characters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 /:@.,#~\n'")
        key = list("T3OeM2aIXsDJp4LwPAgY")
        plainCharacters = []
        keyCharCounter = 0
        for character in cipher:
            characterNum = (characters.index(character) - characters.index(key[keyCharCounter])) % len(characters)
            plainCharacter = characters[characterNum]
            plainCharacters.append(plainCharacter)

            keyCharCounter += 1
            if (keyCharCounter > len(key)-1):
                keyCharCounter = 0

        return "".join(plainCharacters)


#
# VALIDATION
#

# This function checks to see if the day is valid based on the month
def dateCheck(day, month):

    # Check if the month is not between 1 and 12
    if (month < 1 or month > 12):
        return False

    # The max day for each month, from January to December
    maxDayToMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # If the day is greater than the max day of the specified month, return false, else, return true
    if (maxDayToMonth[month-1] < day):
        return False
    else:
        return True

# This function contains different types of string format checks
def formatCheck(value, type):

    # Assume the value is not formatted correctly
    boolFormat = False

    # Phone validation
    if (type == "phone"):

        # Returns false if the number of digits is not exactly 11
        if (len(value) != 11):
            return False

        # Assume true, unless there is a character in the string which is not a digit
        boolFormat = True
        for character in value:
            if (character.isdigit() == False):
                boolFormat = False

    # Name validation
    elif (type == "name"):

        # Assume true, unless there is a character in the string which is a digit
        boolFormat = True
        for character in value:
            if (character.isdigit()):
                boolFormat = False

    # Email validation
    elif (type == "email"):

        # This uses a regular expression
        # It first checks if the email is isolated by itself (\b)
        # Then it checks if it has any number of characters (the username), then an @, then more characters (domain name)
        # then a '.', then at least 2 or more characters (the domain)

        # boolFormat will be either None, or a match object, which is considered 'true'
        boolFormat = re.match(r"\b[\w]+@[A-Za-z\d]+\.[A-Z|a-z]{2,}\b", value)

    # Home address validation
    elif (type == "address"):

        # This uses a regular expression
        # It first checks for a number with a length of 1 to 3 (house number), then space,
        # then any number of characters (house address name), then space,
        # then it checks for more characters (place, street, etc),
        # then it checks for 1 or 2 letters, then a number and allow an extra letter/number (first part of postcode),
        # then finally, after another space, check for a number then 2 letters (second part of postcode)

        # boolFormat will be either None, or a match object, which is considered 'true'
        boolFormat = re.match("[0-9]{1,3} [A-Za-z ]+ [A-Za-z]+ [A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}", value)

    # Time validation
    elif (type == "time"):

        # This uses a regular expression
        # It accepts EITHER 2 then a number between 0 and 3 (hours from 20 to 23), then :,
        # then number between 0 and 5 and then 0 and 9 (minutes)
        # OR a number between 0 to 1, then 0 to 9 (hours from 00 to 19), then :, then 0 to 5, then finally 0 to 9 (minutes)

        # boolFormat will be either None, or a match object, which is considered 'true'
        boolFormat = re.match("(2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])", value)

    # Date validation
    elif (type == "date"):

        # This uses a regular expression
        # It checks if the value is in the format of dd/mm/yy
        boolFormat = re.match("[0-3][0-9]/[0-1][0-9]/[0-9][0-9]", value)

        if (boolFormat == False):
            return boolFormat
        else:
            # Gets the day and month from the string
            day = int(value.split("/")[0])
            month = int(value.split("/")[1])

            # Checks if the day and months are valid (e.g no 40th month, or 72th day, etc)
            boolFormat = dateCheck(day, month)

    # Position validation
    elif (type == "position"):

        # Positions in the business
        positions = ["Manager", "Counter Attendant", "Repairman", "Maintenance"]

        # If the value is equal to one of these positions, return true
        if (value in positions):
            boolFormat = True

    # Convert any 'None' results to 'False'
    if (boolFormat == None):
        boolFormat = False

    # Returns whether or not the value has passed it's validation
    return boolFormat

# This function checks if a value has surpassed its max length
def lengthCheck(value, maxLength):

    # If no max length specified, return true
    if (maxLength == ""):
        return True

    # Assume false, unless the length of the value is not greater than the max length
    boolLength = False
    if (len(value) <= maxLength):
        boolLength = True

    return boolLength

# This function checks a value (of int or float) is between a specified range
def rangeCheck(value, maxRange, minRange=0):

    # Assume false, unless the value is between the max and min range
    boolRange = False
    if (value <= maxRange and value >= minRange):
        boolRange = True

    return boolRange

# This function checks if a value is of the correct type by using exception handling
def typeCheck(value, valueType):

    boolType = False

    # If the value is supposed to be an int, try to cast it into an int, and if it failed, return false
    if (valueType is int):
        try:
            integer = int(value)
            if (type(integer) is valueType):
                boolType = True
        except:
            boolType = False

    # If the value is supposed to be a float, try to cast it into a float, and if it failed, return false
    if (valueType is float):
        try:
            floatValue = float(value)
            if (type(floatValue) is valueType):
                boolType = True
        except:
            boolType = False

    # If the value is supposed to be string, try to cast it into an string, and if it failed, return false
    if (valueType is str):
        try:
            string = str(value)
            if (type(string) is valueType):
                boolType = True
        except:
            boolType = False

    return boolType

# This function checks to see if a foreign key existed in the table where it is a primary key
# Which makes the primary and foreign key fields truly relational;
# a foreign key cannot exist if it doesn't exist as a primary key
def foreignKeyCheck(value, sField):

    # Iterates through the tableIDs in the tableData dictionary
    for tableID in range(len(Table.enumOfTableData)):

        # Iterates through each field in the table
        for field in Table.enumOfTableData[tableID]['fields']:

            # If the field is the same as the foreign key field but is a primary key, get the relevant table
            if (field[0] == sField and field[1][0] == "P"):

                tableName = Table.enumOfTableData[tableID]["name"]
                checkTable = Table(tableName)

    # Verify that the record exists with the correct key
    return checkTable.verifyRecordExistence(value)


#
# FRONT END
#

# Program starts with this function
def main():
    # Introductory message
    print("| | | Heard's Computer Cafe | | |" + "\n")

    # Commence backup every time the program is run
    backup()

    # Go to the login function
    login()

# This function makes a backup of the database
def backup():

    # Opens the backup file in write mode
    backupFile = open("db_backup.txt", "w")

    # Attempts to open the file, if it can't, create a new one, then finally open the file
    try:
        file = open("db.txt")
    except:
        file = open("db.txt", "w")
    finally:
        file = open("db.txt")

        # Write the contents of the main file into the backup file
        backupFile.write(file.read())

        file.close()

# This function allows the user to login into their account and access the rest of the program
def login():

    # Get the account details table
    loginTable = Table("Account Details")

    # If there are no accounts in the table, then go through the create account process
    if (loginTable.tableLength() == 0):
        print("No Accounts Created, will go through the process of account creation.")
        return createAccount()

    # Login section
    print("--- Login ---")
    print("Type 'exit' at any point to quit the program.")
    username = input("Enter username: ")

    # If exit inputted into username, then exit
    if (username == "exit"): return exit()

    password = input("Enter password: ")

    # If exit inputted into password, then exit
    if (password == "exit"): return exit()

    # If the record for the account wasn't found that contained both the correct username and password, then the details were incorrect
    while (loginTable.verifyRecordExistence(username, 2) == False or loginTable.verifyRecordExistence(password, 3) == False):
        print("Username or Password invalid, please try again.")
        print("Type 'exit' at any point to quit the program.")
        username = input("Enter username: ")

        # If exit inputted into username, then exit
        if (username == "exit"): return exit()

        password = input("Enter password: ")

        # If exit inputted into password, then exit
        if (password == "exit"): return exit()

    # Forms a dictionary containing both the account and staff details of the user
    accountData = updateAccountData(username)

    # Go to home page
    return tablesMenu(accountData)

# This function brings up the list of options a user can do
def tablesMenu(account, showTable=True):

    # This lists all the tables in the table class by getting its 'metadata'
    listOfTables = []
    for table in Table.enumOfTableData.values():

        # Prevents a user with the position of 'Maintenance' to gain access to unauthorised tables
        if (account['staffDetails'][6] == "Maintenance" and table['name'] not in ["Computer Status"]):
            continue

        # Prevents a user with the position of 'Repairman' to gain access to unauthorised tables
        if (account['staffDetails'][6] == "Repairman" and table['name'] not in ["Repair Reservations", "Customer Details"]):
            continue

        # Prevents a user with the position of 'Counter Attendant' to gain access to unauthorised tables
        if (account['staffDetails'][6] == "Counter Attendant" and table['name'] not in ["Computer Reservations","Customer Details", "Stocks", "Computer Status"]):
            continue

        # Creates puts the index and table name in it's own array
        tableData = [len(listOfTables), table['name']]

        # Insert the tableData into the list (2d array)
        listOfTables.append(tableData)

    # If the account belongs to the manager role, give the option to create an account and reset a password
    if (account['staffDetails'][6] == "Manager"):
        listOfTables.append([len(listOfTables), "Create Account"])
        listOfTables.append([len(listOfTables), "Reset Account Password"])

    # Output the tables that can be selected, and also the option to access personal details and to close the program
    if (showTable == True):
        formattedListOfTables = [f"\n({table[0]}): {table[1]}" for table in listOfTables]
        print(f"Tables: {''.join(formattedListOfTables)}\n\nOr ({len(listOfTables)}): Personal Details Program\nOr ({len(listOfTables)+1}): Close Program")

    # Checks to see if the input is within the number of tables and the extra close program option
    tableSelection = input("Select table by index or by name: ")

    # Checks to see if the tableSelection is not the name of the table. If it is, it can directly go there, making
    # it easier for the user to navigate.
    if (tableSelection not in [tableData[1] for tableData in listOfTables]):

        # Try to interpret the input, if it fails, recursively call the home page function, except do not send the
        # table again
        try:
            tableSelection = int(tableSelection)
        except:
            print("Input is not a number. Please try again.")
            return tablesMenu(account, False)

        # Check if the range of the selected table is invalid
        while (int(tableSelection) not in range(0, len(listOfTables) + 2)):
            print(f"Input is not in the range of 0 to {len(listOfTables) + 2}. Please try again.")
            tableSelection = input("Select Table by index: ")

            try:
                tableSelection = int(tableSelection)
            except:
                print("Input is not a number. Please try again.")
                return tablesMenu(account, False)

        # Create account option only for Manager
        if (tableSelection == len(listOfTables)-2 and account['staffDetails'][6] == "Manager"):
            return createAccount()

        # Reset account password option only for Manager
        if (tableSelection == len(listOfTables)-1 and account['staffDetails'][6] == "Manager"):
            return resetAccountPassword(account)

        # Personal details page for all users
        if (tableSelection == len(listOfTables)):
            return personalDetails(account)

        # If the last option is chosen, exit program
        if (tableSelection == (len(listOfTables)+1)):
            return exit()

        # Converts table id into table name
        tableSelection = listOfTables[int(tableSelection)][1]

    # Once table is selected, go to the table screen
    tableManipulation(tableSelection, account)

# This function goes through the process of creating an account (requires a staff record and an account record)
def createAccount():
    # Get the login and staff tables
    loginTable = Table("Account Details")
    staffTable = Table("Staff Details")

    # Goes through the record creation process with staff record first then the account record
    createRecordProcess(staffTable)
    createRecordProcess(loginTable)

    # Go to login afterwards
    login()

# This function allows for the manager to reset a user's password quickly
def resetAccountPassword(account):

    # Gets the relevant tables
    accountTable = Table("Account Details")
    staffTable = Table("Staff Details")

    # Prints both of the tables
    print(f"{staffTable.tableName}:")
    staffTable.listToViewable()

    print(f"{accountTable.tableName}:")
    accountTable.listToViewable()

    # Requests the index of the user to delete
    print("Choose Account Password to reset by index.")

    try:
        choice = int(input())
    except:
        print("Input is not an integer. Please try again.")
        return resetAccountPassword(account)

    if (choice > accountTable.tableLength() or choice < 0):
        print("Input is out of range. Please try again.")
        return  resetAccountPassword(account)

    # Verification technique to prevent slip ups
    print(f"Are you sure you want to reset {accountTable.findRecord('accountID', choice)[2]}'s account? (Y/N)")
    confirmation = input()

    if (confirmation.lower() not in ["yes", "y"]):
        print("Cancelled reset.")
        return tablesMenu(account)

    # Amend the record
    amendRecordProcess(accountTable, account, choice, "password", "Password")
    print("Successfully reset password!")

    # Go back to the home page
    return tablesMenu(account)

# This function updates the account dictionary if an update is made to the user's staff or account details in the database
def updateAccountData(username):

    # Get the login table and find the user's account record
    loginTable = Table("Account Details")
    account = loginTable.findRecord("username", username)

    # Get the staff table and find the user's staff record
    staffTable = Table("Staff Details")
    staffDetails = staffTable.findRecord("staffID", account[1])

    # Combine them into a dictionary, and return it
    accountData = {"account": account, "staffDetails": staffDetails}
    return accountData

# This function creates the personal user details page
def personalDetails(account):

    # Get relevant tables
    staffTable = Table("Staff Details")
    accountTable = Table("Account Details")

    # Uses the account data to retrieve the personal staff details
    print(", ".join(staffTable.tableFields))
    print(", ".join(account["staffDetails"]))

    # Uses the account data to retrieve the personal account details
    print(", ".join(accountTable.tableFields))
    print(", ".join(account["account"]))

    # Options
    print("0: Amend value, 1: Change Password, 2: Back to Table Selection")

    # Checks to see if a valid input is made (is int)
    try:
        choice = int(input())
    except:
        print("Input is not a valid index. Please try again.")
        return personalDetails(account)

    # Checks to see if a valid input is made (is between the valid range of options)
    if (choice > 2 or choice < 0):
        print("Input is not a valid index. Please try again.")
        return personalDetails(account)

    # Amend value
    if (choice == 0):
        print("0: Amend Staff Details, 1: Amend Account Details")

        # Checks to see if a valid input is made (is int)
        try:
            tableChoice = int(input())
        except:
            print("Input is not a valid index. Please try again.")
            return personalDetails(account)

        # Checks to see if a valid input is made (is between the valid range of options)
        if (tableChoice > 1 or tableChoice < 0):
            print("Input is not a valid index. Please try again.")
            return personalDetails(account)

        # Amends staff details, goes through the process of amendment
        if (tableChoice == 0):
            amendRecordProcess(staffTable, account, int(account["staffDetails"][0]))

        # Amends account details, goes through the process of amendment
        elif (tableChoice == 1):
            amendRecordProcess(accountTable, account, int(account["account"][0]))

    # Change password
    elif (choice == 1):
        # Input a new password
        print("Enter your new password: ")
        newPassword = input()

        # Input the same password again: type of verification
        print("Enter your new password again: ")
        passwordReattempt = input()

        # Confirm that the password is the same as the reattempt. If not, continue to try until they are equal
        while (newPassword != passwordReattempt):
            print("Passwords are not the same. Try again.")

            print("Enter your new password: ")
            newPassword = input()
            print("Enter your new password again: ")
            passwordReattempt = input()

        # Make the amendment to the account table
        amendRecordProcess(accountTable, account, int(account["account"][0]), "password", newPassword)

    # Return to home page
    elif (choice == 2):
        return tablesMenu(account)

    # Updates the account dictionary, and also returns back to the personal user details page
    account = updateAccountData(account['account'][2])
    personalDetails(account)

# This function goes to the database viewer page, based on the table input and user account
def tableManipulation(tableSelection, account):

    # Instantiates table
    table = Table(tableSelection)

    # Prints the table name, then the table
    print(f"{table.tableName}:")
    table.listToViewable()

    # Options
    print("0: Create Record, 1: Delete Record, 2: Amend Record, 3: Search Record, 4: Back to Table Selection")

    # Attempt to get an input within the option indexes
    actionSelection = input()

    # Test for actionSelection is an int
    try:
        actionSelection = int(actionSelection)
    except:
        print("Input is not an integer. Try again.")
        return tableSelection(table, account)

    # Test for actionSelection is an int within range of the options
    while (actionSelection not in range(0, 5)):
        print("Not valid. Try again.")
        actionSelection = input()

        try:
            actionSelection = int(actionSelection)
        except:
            print("Input is not an integer. Try again.")
            return tableSelection(table, account)

    # Create record
    if (actionSelection == 0):

        # Check if user has required permissions to change data in table
        if ((table.tableName == "Computer Status" and account['staffDetails'][6] == "Counter Attendant") or (table.tableName == "Transaction History")):
            print("This table cannot be amended.")
            return tableManipulation(tableSelection, account)

        createRecordProcess(table, account)
        return tableManipulation(tableSelection, account)

    # Delete record
    elif (actionSelection == 1):

        # Check if user has required permissions to change data in table
        if ((table.tableName == "Computer Status" and account['staffDetails'][6] == "Counter Attendant") or (table.tableName == "Transaction History")):
            print("This table cannot be amended.")
            return tableManipulation(tableSelection, account)

        deleteRecordProcess(table, account)
        return tableManipulation(tableSelection, account)

    # Amend record
    elif (actionSelection == 2):

        # Check if user has required permissions to change data in table
        if ((table.tableName == "Computer Status" and account['staffDetails'][6] == "Counter Attendant") or (table.tableName == "Transaction History")):
            print("This table cannot be amended.")
            return tableManipulation(tableSelection, account)

        amendRecordProcess(table, account)
        return tableManipulation(tableSelection, account)

    # Search record
    elif (actionSelection == 3):

        searchRecordProcess(table)
        return tableManipulation(tableSelection, account)

    # Goes back to table selection
    elif (actionSelection == 4):
        return tablesMenu(account)

# This goes through the process of creating a record with the user
def createRecordProcess(table, account=0):

    # Creates the parameters list to input into the Table class' createRecord method
    parameters = []
    print("Enter parameters: ")

    # Gets the data for each field for the table skipping the first element
    # since the first element is auto generated (primary key)
    fieldsData = table.tableFieldData[1:len(table.tableFieldData)]

    # Iterates through each field's data
    for data in fieldsData:

        # Combines them into a dictionary for easy use
        fieldData = {
            "name": data[0],
            "keyType": data[1][0],
            "classType": data[1][1],
            "maxLength": data[1][2],
            "defaultValue": data[1][3],
            "additionalValidation": data[1][4],
            "isRequired": data[1][5]
        }

        # If there is additional validation, assign extra data
        if (fieldData["additionalValidation"] != ""):
            fieldData["validationType"] = data[1][4][0]
            fieldData["argument"] = data[1][4][1]

        # Check for a default value, if not empty, alert the user
        if (fieldData["defaultValue"] != ""):
            print(f"This parameter has a default of {fieldData['defaultValue']}. Enter empty to leave it at default.")

        # Check is the parameter is not required, if so, alert the user
        if (fieldData["isRequired"] == False):
            print(f"This parameter ({fieldData['defaultValue']}) is not required. Enter empty to leave it at 'None'.")

        if (fieldData["additionalValidation"] != ""):
            if (fieldData["argument"] == "position"):
                print("This parameter has the select choices of 'Manager', 'Counter Attendant', 'Repairman', and 'Maintenance'.")

            if (fieldData["argument"] == "address"):
                print("This parameter has the format of: (Street Num) (Residential Name) (Residence Type) (City) (Outcode) (Incode)")

        # Get input value for field
        print(f"What is the {fieldData['name']}? ")
        attribute = input()

        # If input is empty and default value is not empty, append default value and go to the next field to input
        if (attribute == "" and fieldData["defaultValue"] != ""):
            parameters.append(str(fieldData["defaultValue"]))
            continue

        # If input is empty and field value is not required, append "None" and go to the next field to input
        if (attribute == "" and fieldData["isRequired"] == False):
            parameters.append("None")
            continue

        # If the field is a foreign key, make sure that the primary key exists
        if (fieldData["keyType"] == "F"):
            while foreignKeyCheck(attribute, fieldData['name']) == False:
                print("Invalid Key, please try again.")
                print(f"What is the {fieldData['name']}? ")
                attribute = input()

        # Check that the type is correct with the field data
        while typeCheck(attribute, fieldData["classType"]) == False:
                print("Invalid Type, please try again.")
                print(f"What is the {fieldData['name']}? ")
                attribute = input()

        # Check that the length is within the max length in field data
        while lengthCheck(attribute, fieldData["maxLength"]) == False:
            print("Invalid Length, please try again.")
            print(f"What is the {fieldData['name']}? ")
            attribute = input()

        # Additional validation
        if (fieldData["additionalValidation"] != ""):

            # Validate the input with its respective format check
            if (fieldData["validationType"] == "format"):
                while formatCheck(attribute, fieldData["argument"]) == False:
                    print("Invalid Format, please try again.")
                    print(f"What is the {fieldData['name']}? ")
                    attribute = input()

            # Validate the input with its respective range check
            if (fieldData["validationType"] == "range"):

                attribute = int(attribute) if fieldData["classType"] is int else float(attribute)

                while rangeCheck(attribute, fieldData["argument"]) == False:
                    print("Invalid Range, please try again.")
                    print(f"What is the {fieldData['name']}? ")
                    attribute = input()

                    attribute = int(attribute) if fieldData["classType"] is int else float(attribute)

                # Convert attribute back to string
                attribute = str(attribute)

        # If all checks are passed, append the attribute to list
        parameters.append(attribute)

    # After getting all the data, create record
    table.createRecord(parameters)

    # Make transactionHistory record
    if (table.tableName == "Stocks"):
        transactionHistoryAmend(account, table.findRecord("stockName", parameters[0])[0], f"'Created Record '{parameters[0]}'.'")

# This goes through the process of amending a record with the user
def amendRecordProcess(table, account, index=None, field=None, attribute=None):

    # If index already specified, do not request an input from user
    if (index == None):
        # Get the index of record to amend
        print("Select index of record: ")
        index = int(input())

    # If field already specified, do not request an input from user
    if (field == None):
        # Lists the fields in the table, then asks the user for the one to change
        listOfFields = '\n'.join(table.tableFields)
        print(f"Select field to change:\n{listOfFields}")

        # Attempts to get a valid field name
        field = input()
        while (field not in listOfFields):
            print("Invalid. Try again (it is the name of the field, not index)")
            field = input()

    # Gets the relevant field data by the name of the field
    fieldsData = table.tableFieldData[[fieldData[0] for fieldData in table.tableFieldData].index(field)]

    # Combines them into a dictionary for easy use
    fieldData = {
        "name": fieldsData[0],
        "keyType": fieldsData[1][0],
        "classType": fieldsData[1][1],
        "maxLength": fieldsData[1][2],
        "defaultValue": fieldsData[1][3],
        "additionalValidation": fieldsData[1][4],
        "isRequired": fieldsData[1][5]
    }

    # If there is additional validation, assign extra data
    if (fieldData["additionalValidation"] != ""):
        fieldData["validationType"] = fieldsData[1][4][0]
        fieldData["argument"] = fieldsData[1][4][1]

    # If attribute already specified, do not request an input from user
    if (attribute == None):

        # If input is empty and default value is not empty, append default value and go to the next field to input
        if (fieldData["defaultValue"] != ""):
            print(f"This parameter has a default of {fieldData['defaultValue']}. Enter empty to leave it at default.")

        # If input is empty and field value is not required, append "None" and go to the next field to input
        if (fieldData["isRequired"] == False):
            print(f"This parameter ({fieldData['defaultValue']}) is not required. Enter empty to leave it at 'None'.")

        # Gets the value to amend the field with
        print(f"Change the value in {field} to: ")
        attribute = input()

    # If input is empty and default value is not empty, append default value and go to the next field to input
    if (attribute == "" and fieldData["defaultValue"] != ""):
        attribute = fieldData["defaultValue"]

    # If input is empty and field value is not required, append "None" and go to the next field to input
    if (attribute == "" and fieldData["isRequired"] == False):
        attribute = "None"

    # If the field is a foreign key, make sure that the primary key exists
    if (fieldData["keyType"] == "F"):
        while foreignKeyCheck(attribute, fieldData['name']) == False:
            print("Invalid Key, try again.")
            print(f"What is the {fieldData['name']}? ")
            attribute = input()

    # Check that the type is correct with the field data
    while typeCheck(attribute, fieldData["classType"]) == False:
        print("Invalid Type, try again.")
        print(f"What is the {fieldData['name']}? ")
        attribute = input()

    # Check that the length is within the max length in field data
    while lengthCheck(attribute, fieldData["maxLength"]) == False:
        print("Invalid Length, try again.")
        print(f"What is the {fieldData['name']}? ")
        attribute = input()

    # Additional validation
    if (fieldData["additionalValidation"] != ""):

        # Validate the input with its respective format check
        if (fieldData["validationType"] == "format"):
            while formatCheck(attribute, fieldData["argument"]) == False:
                print("Invalid Format, try again.")
                print(f"What is the {fieldData['name']}? ")
                attribute = input()

        # Validate the input with its respective range check
        if (fieldData["validationType"] == "range"):

            attribute = int(attribute) if fieldData["classType"] is int else float(attribute)

            while rangeCheck(attribute, fieldData["argument"]) == False:
                print("Invalid Range, try again.")
                print(f"What is the {fieldData['name']}? ")
                attribute = input()

                attribute = int(attribute) if fieldData["classType"] is int else float(attribute)

            # Convert attribute back to string
            attribute = str(attribute)

    # Amends the record, then goes back to table screen
    table.amendRecord(index, field, attribute)

    # Make transactionHistory record
    if (table.tableName == "Stocks"):
        transactionHistoryAmend(account, table.findRecord(field, attribute)[0], f"'Amended Record '{table.findRecord(field, attribute)[0]}'s {field} to: {attribute}'.'")

# This goes through the process of deleting a record with the user
def deleteRecordProcess(table, account):

    # Select the index of the record to remove
    print("Select index of record: ")
    index = input()

    # Checks to see if a valid input is made (is int)
    try:
        index = int(index)
    except:
        print("Input is not an integer. Please try again.")
        deleteRecordProcess(table, account)

    # Checks to see if a valid input is made (is between the valid range of options)
    if (index > table.tableLength()-1 or index < 0):
        print("Input is not in range. Please try again.")
        deleteRecordProcess(table, account)

    # Gets the primary field of the selected table
    primaryField = table.tableFieldData[0][0]

    # Searches through the enumeration of table data for records that may be affected by the deletion of the current record
    affectedRecords = []
    for tableID in range(len(Table.enumOfTableData)):
        for field in Table.enumOfTableData[tableID]['fields']:
            # Check if field is the same as the primary key field but it is a foriegn key
            if (field[0] == primaryField and field[1][0] == "F"):

                # Get the table name, the table, and attempt to find the record
                tableName = Table.enumOfTableData[tableID]["name"]
                aTable = Table(tableName)
                foundRecord = aTable.findRecord(primaryField, index)

                # If found, append to affected records to alert the user
                if (foundRecord != -1):
                    affectedRecords.append([tableName, foundRecord])

    # Alert the user if there are any affected records
    if (len(affectedRecords) > 0):
        print("Warning! This deletion will also delete the following records:")
        for affectedData in affectedRecords:
            print(f"({affectedData[0]}): {affectedData[1]}")

    # Verify with user whether they wish to delete the record(s)
    print("\nAre you sure you want to delete this record? (Y/N)")
    confirmation = input()

    if (confirmation.lower() not in ["yes", "y"]):
        return print("Cancelled deletion.")

    # Iterate through each record and delete them in their respective tables
    for toDeleteData in affectedRecords:
        dTable = Table(toDeleteData[0])
        dTable.deleteRecord(int(toDeleteData[1][0]))

    # Delete the record, then go back to table screen
    table.deleteRecord(index)

    # Inform user
    print("Successfully deleted record(s).")

    # Make transactionHistory record
    if (table.tableName == "Stocks"):
        transactionHistoryAmend(account, index, f"'Deleted Record '{index}'.'")

# This function goes through the process of searching for a record with the user
def searchRecordProcess(table):

    # Lists the fields in the table, then asks the user for the one to search for
    listOfFields = '\n'.join(table.tableFields)
    print(f"Select field to search for:\n{listOfFields}")

    # Attempts to get a valid field name
    field = input()
    while (field not in listOfFields):
        print("Invalid. Try again (it is the name of the field, not index)")
        field = input()

    # Gets the search value
    searchValue = input("Input search value: ")

    # Searches for the record
    record = table.findRecord(field, searchValue)

    # If not found, return failure message, else, print it
    if (record == -1):
        print(f"Record wasn't found. Did you mean to type '{searchValue}'")
    else:
        print(" ".join(record))

# This function is used to add records to the transaction history automatically
def transactionHistoryAmend(account, stockID, change):
    # Get transaction table
    transactionTable = Table("Transaction History")

    # Get accountID, then create record
    accountID = account["account"][0]
    transactionTable.createRecord([accountID, stockID, change])

# Start the program
main()
