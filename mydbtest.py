# Create a b-tree database. Uses bsddb3 
# DB_SIZE is set to 3 for testing purposes. Change to 100000 later.

import sys
import easygui as eg
from timeit import Timer

from bsddb3 import db
from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')

# Not sure if it needs to be in this directory,
# Just went with the example for now
DB_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 3  # Change to 100000 later
SEED = 10000000
database_exists = False # bool does database already exist
cur = None # cursor must be accessible by all functions
DATABASE = None # Not sure if this needs to be here, but playing it safe for now

def key_record(key, cur):
    """
    Retrieve a record with a given key.
    Input key should be a string, which gets encoded to bytes.
    Returns <key,data> pair is exists.
    Returns None if key does not exist.
    """
    # Change key from string to bytes
    bytes_key = key.encode('utf-8')
    data = cur.set(bytes_key)
    if (data):
        print("Number of records retrieved: 1")
        print(data)

        # Open answers file.
        answers = open('answers','a')
        # Get the data portion of the <key,data> pair
        strdata = data[1]
        # Convert from bytes to a string.
        strdata = strdata.decode('utf-8')
        # Append to answers file.
        answers.write(key)
        answers.write('\n')
        answers.write(strdata)
        answers.write('\n')
        answers.write('\n')
        return(data)
    else:
        print (key, "was not found.")
        print ("Number of records retrieved: 0")
        return ("Key not found")

def main ():
    # gets the type from the arguements used to run the program
    type = sys.argv

    # Check if there is an existing database
    try:
        print ("Opening existing database.")
        DATABASE = db.DB()
        DATABASE.open("sample_db")
    except:
        DATABASE = db.DB()
        # Create a database based on type 
        print ("Database doesn't exist. Creating a new one.")
        if type == BTREE:
            DATABASE.open("sample_db", None, db.DB_BTREE, db.DB_CREATE)
            print("using BTREE")
        elif type == HASH:
            DATABASE.open("sample_db", None, db.DB_HASH, dn.DB_CREATE)
            print("using Hashtable")

    # This is taken from python example shown in lab, with changes for python3
    # Add records to the database
    lib.set_seed(SEED)
    print(" ")
    print("Printing <Key, Value> pairs.")
    for index in range(DB_SIZE):
        krng = 64 + (lib.get_random() % 64)
        key = ""
        for i in range(krng):
            key = key + str(chr(lib.get_random_char()))
        vrng = 64 + (lib.get_random() % 64)
        value = ""
        for i in range(vrng):
            value = value + str(chr(lib.get_random_char()))
        print("Key: ",key)
        print("Value: ",value)
       
        # Change the string into bytes.
        key = key.encode('utf-8')
        value = value.encode('utf-8')
        # Add key,value pair to database only if key is unique.
        if (DATABASE.exists(key) == False):
            DATABASE.put(key,value)
        else:
            print("This key is not unique. Pair was not added.")
        print(" ")

    # Create a cursor
    cur = DATABASE.cursor()
    
    # Time the key_record function.
    time = Timer(lambda: key_record(key.decode('utf-8'), cur)).timeit(number=1)
    print("Time in microseconds: ", (time*100000))

    print("\n")
    print("Here is a key_record call that will fail: ")
    time = Timer(lambda: key_record("notakey", cur)).timeit(number=1)
    print("Time in microseconds: ", (time*1000000))

    # Close the database
    try:
        cur.close()
        DATABASE.close()
    except Exception as e:
        print(e)

def GuiCreateDatabase():
    """
    Creates and populates the database
    """
    # gets the type from the arguements used to run the program
    type = sys.argv
    print("Type is {}".format(type))
    # Check if there is an existing database
    try:
        print ("Opening existing database.")
        DATABASE = db.DB()
        DATABASE.open("sample_db")
        # Database should not exist, if you hit this something is wrong
        eg.msgbox("Reaching this box should be impossible")
    except:
        DATABASE = db.DB()
        # Create a database based on type 
        print ("Database doesn't exist. Creating a new one.")
        if "BTREE" in type:
            DATABASE.open("sample_db", None, db.DB_BTREE, db.DB_CREATE)
            print("using BTREE")
        elif "HASH" in type:
            DATABASE.open("sample_db", None, db.DB_HASH, dn.DB_CREATE)
            print("using Hashtable")
        else:
            eg.msgbox("Invalid type on execution, format should be python3 mydbtest.py BTREE/HASH")
            return

    # This is taken from python example shown in lab, with changes for python3
    # Add records to the database
    lib.set_seed(SEED)
    print(" ")
    print("Printing <Key, Value> pairs.")
    for index in range(DB_SIZE):
        krng = 64 + (lib.get_random() % 64)
        key = ""
        for i in range(krng):
            key = key + str(chr(lib.get_random_char()))
        vrng = 64 + (lib.get_random() % 64)
        value = ""
        for i in range(vrng):
            value = value + str(chr(lib.get_random_char()))
        print("Key: ",key)
        print("Value: ",value)
       
        # Change the string into bytes.
        key = key.encode('utf-8')
        value = value.encode('utf-8')
        # Add key,value pair to database only if key is unique.
        if (DATABASE.exists(key) == False):
            DATABASE.put(key,value)
        else:
            print("This key is not unique. Pair was not added.")
        print(" ")

    # Create a cursor
    return DATABASE.cursor()

def GuiRetrieveWithKey():
    """
    Retrieve records with a given key. This could be integrated into the
    record_key function, but I wanted to make sure the main() code still
    ran, so we can do a renaming later if we want.
    """
    msg = "Please enter the key you wish to search for"
    title = "Retrieve data with given key"
    searchkey = eg.enterbox(msg, title)
    if searchkey == None:
        eg.msgbox("Operation cancelled.")
        return
    msg = key_record(searchkey, cur)
    title = "Result"
    eg.msgbox(msg, title)
        

def GuiRetrieveWithData():
    """
    Retrieve records with a given data
    """
    pass

def GuiRetrieveWithRange():
    """
    Retrieve records with a given range of key values
    """
    pass

def GuiDestroyDatabase():
    """
    Destroy the database
    """
    pass

try:
    print ("Opening existing database.")
    DATABASE = db.DB()
    DATABASE.open("sample_db")
    eg.msgbox("Existing database found, opening existing database")
    database_exists = True
    cur = DATABASE.cursor()
except:
    eg.msgbox("No existing database found. Be sure to create a new one.")
    database_exists = False
    
while True:
    msg = "CMPUT 291 Project 2, by Victoria Bobey, Sarah Morris, and Eldon Lake"
    title = "mydbtest"
    choices = ["Create and populate the database",
               "Retrieve records with a given key",
               "Retrieve records with a given data",
               "Retrieve records wtih a given range of key values",
               "Destroy the database"]
    choice = eg.choicebox(msg, title, choices)
    if choice == choices[0]:
        if not database_exists:
            cur = GuiCreateDatabase()
            database_exists = True
        else:
            eg.msgbox("Database already exists. Destroy the old database before attempting to create a new one.")
    elif choice == choices[1]:
        if database_exists:
            GuiRetrieveWithKey()
        else:
            eg.msgbox("Error! Must create database first.")
    elif choice == choices[2]:
        if database_exists:
            GuiRetrieveWithData()
        else:
            eg.msgbox("Error! Must create database first.")
    elif choice == choices[3]:
        if database_exists:
            GuiRetrieveWithRange()
        else:
            eg.msgbox("Error! Must create database first.")
    elif choice == choices[4]:
        if database_exists:
            GuiDestroyDatabase()
        else:
            eg.msgbox("Error! Must create database first.")

    msg = "Do you want to continue?"
    title = "Continue?"
    if eg.ccbox(msg, title, ('Continue', 'Exit')): # Continue/Cancel dialog
        pass # user chose Continue
    else:
        con.close()
        sys.exit(0) # user chose Cancel

if __name__ == "__main__":
    main()
