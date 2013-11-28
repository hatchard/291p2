# Create a b-tree database. Uses bsddb3 
# DB_SIZE is set to 3 for testing purposes. Change to 100000 later.

import sys
import easygui as eg
import time

import random # For testing purposes

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

"""
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
    
    for index in range(DB_SIZE):
        krng = 64 + (lib.get_random() % 64)
        key = ""
        for i in range(krng):
            key = key + str(chr(lib.get_random_char()))
        vrng = 64 + (lib.get_random() % 64)
        value = ""
        for i in range(vrng):
            value = value + str(chr(lib.get_random_char()))
       
        # Change the string into bytes.
        key = key.encode('utf-8')
        value = value.encode('utf-8')
        # Add key,value pair to database only if key is unique.
        if (DATABASE.exists(key) == False):
            DATABASE.put(key,value)
        else:
            print("This key is not unique.")

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
"""

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
            eg.msgbox("Btree database created.")

        elif "HASH" in type:
            DATABASE.open("sample_db", None, db.DB_HASH, db.DB_CREATE)
            print("using Hashtable")
        else:
            eg.msgbox("Invalid type on execution, format should be python3 mydbtest.py BTREE/HASH")
            return

    # This is taken from python example shown in lab, with changes for python3
    # Add records to the database
    lib.set_seed(SEED)

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
            print(key.decode('utf-8'), "cannot be added as it is a duplicate.")

    # Create a cursor
    return DATABASE.cursor()

def GuiRetrieveWithKey():
    """
    Retrieve records with a given key.
    """
    msg = "Please enter the key you wish to search for"
    title = "Retrieve data with given key"
    searchkey = eg.enterbox(msg, title)
    if searchkey == None:
        eg.msgbox("Operation cancelled.")
        return
        
    # >>>> Enable the following 2 lines for testing: <<<<<<
    # searchkey = Testing(1)
    # print (searchkey)
    
    # Change the key from string to bytes:
    bytes_key = searchkey.encode('utf-8')

    # Run the query, taking time before and after.
    time_before = time.time()
    data = cur.set(bytes_key)
    time_after = time.time()

    # Get time in microseconds
    runtime = (time_after - time_before) * 100000
    
    # Results found
    if (data):
        # Open answers file.
        answers = open('answers','a')
        # Get the data portion of the <key,data> pair
        strdata = data[1]
        # Convert from bytes to a string.
        strdata = strdata.decode('utf-8')
        # Append to answers file.
        answers.write(searchkey)
        answers.write('\n')
        answers.write(strdata)
        answers.write('\n')
        answers.write('\n')
        text = ("Key input: \n{} \nData value found: \n{} \nNumber of records retrieved: 1 \nTime: {} microseconds.".format(searchkey, strdata, runtime))
    # No results
    else:
        text = ("No results found for the following key: \n{} \nNumber of records retrieved: 0 \nTime: {} microseconds".format(searchkey, runtime))

    msg = "Results:" 
    title = "Retrieve With Key"
    eg.textbox(msg, title, text)
        

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
    # Close the existing database handle.
    DATABASE.close()

    # Open a new database handle and drop the database.
    db_destroy = db.DB()
    try:
        db_destroy.remove("sample_db")
        eg.msgbox("Database was successfully dropped.")
        db_destroy.close()
    except Exception as e:
        eg.msgbox(e)

    return

def Testing(val_type):
    """
    Get a random key or data value from the database.
    This is for testing the queries.
    ** If you want a random key val_type = 1.
    If you want a random data value val_type = 2.
    """
    # Get all pairs in database and add them to a list.
    all_pairs = []
    iter = cur.first()
    while iter:
        all_pairs.append(iter)
        iter = cur.next()

    # Get a random pair from the list.
    index = random.randint(0, (len(all_pairs)-1))
    random_pair = all_pairs[index]

    # Get the key or data part.
    if val_type == 1:
        random_key = random_pair[0]
        # Decode back to a string.
        random_key = random_key.decode('utf-8')
        return random_key
    elif val_type == 2:
        random_data = random_pair[1]
        # Decode back to a string.
        random_data = random_data.decode('utf-8')
        return random_data
    else:
        # Should never be in here.
        raise Exception ("Not a valid val_type input to Testing.")

try:
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
            database_exists = False
        else:
            eg.msgbox("Error! Must create database first.")

    msg = "Do you want to continue?"
    title = "Continue?"
    if eg.ccbox(msg, title, ('Continue', 'Exit')): # Continue/Cancel dialog
        pass # user chose Continue
    else:
        DATABASE.close()
        sys.exit(0) # user chose Cancel

"""
if __name__ == "__main__":
    main()
"""
