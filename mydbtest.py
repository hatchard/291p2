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
DB_FILE = "/tmp/elake/sample_db"
SDB_FILE = "/tmp/elake/IndexFile"
DB_SIZE = 100000
SEED = 10000000
database_exists = False # bool does database already exist
cur = None # cursor must be accessible by all functions
DATABASE = None # Not sure if this needs to be here, but playing it safe for now

def GuiIndexData():
    """
    Retrieve records with a given data
    """
    msg = "Please enter the data you would like to search for"
    title = "Retrieve key with given data"
    searchdata = eg.enterbox(msg, title)

    if searchdata == None:
        eg.msgbox("Operation cancelled.")
        return

    # Change the data from string to bytes:
    bytes_data = searchdata.encode('utf-8')

    time_before = time.time()
    key = sec_cur.set(bytes_data)
    time_after = time.time()

    # Get time in microseconds
    runtime = (time_after - time_before) * 1000000

    # Results found
    if (key):
        # Append to answers file.
        answers.write(key[1].decode('utf-8'))
        answers.write('\n')
        answers.write(key[0].decode('utf-8'))
        answers.write('\n')
        answers.write('\n')
        text = ("Data input: \n{} \nKey value found: \n{} \nNumber of records retrieved: 1 \nTime: {} microseconds.".format(key[1].decode('utf-8'), key[0].decode('utf-8'), runtime))
    # No results
    else:
        text = ("No results found for the following data: \n{} \nNumber of records retrieved: 0 \nTime: {} microseconds".format(searchdata, runtime))

    msg = "Results:"
    title = "Retrieve With Data"
    eg.textbox(msg, title, text)

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
        DATABASE.open(DB_FILE)
        # Database should not exist, if you hit this something is wrong
        eg.msgbox("Reaching this box should be impossible")
    except:
        # Create a database based on type 
        DATABASE = db.DB()
        print ("Database doesn't exist. Creating a new one.")
        if "BTREE" in type or "btree" in type or "indexfile" in type:
            DATABASE.open(DB_FILE, None, db.DB_BTREE, db.DB_CREATE)
            if "indexfile" in type or "IndexFile" in type:
                SEC_DB = db.DB()
                SEC_DB.open(SDB_FILE, None, db.DB_BTREE, db.DB_CREATE)
                eg.msgbox("Creating Indexed Database. Please wait.")
            else:
                print("btree database created")
                eg.msgbox("Creating Btree Database. Please wait.")
        elif "HASH" in type or "hash" in type:
            DATABASE.open(DB_FILE, None, db.DB_HASH, db.DB_CREATE)
            eg.msgbox("Creating Hash Table Database. Please wait.")
        else:
            eg.msgbox("Invalid type on execution, format should be ./mydbtest.py btree or hash or indexfile")
            return

    # This is taken from python example shown in lab, with changes for python3
    # Add records to the database
    lib.set_seed(SEED)

    #for index in range(DB_SIZE):
    index = 1
    while index <= DB_SIZE:
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
            if "indexfile" in type:
                SEC_DB.put(value, key)
        else:
            while (DATABASE.exists(key) == True):
                print(key.decode('utf-8'), "cannot be added as it is a duplicate.")
                krng = 64 + (lib.get_random() % 64)
                key = ""
                for i in range(krng):
                    key = key + str(chr(lib.get_random_char()))
                key = key.encode('utf-8')
            if "indexfile" in type:
                SEC_DB.put(value, key)
            DATABASE.put(key,value)
        index = index + 1
   
    if "indexfile" in type:
        SEC_DB.close()
    print("Length of Database: ", len(DATABASE))
    DATABASE.close()
    return

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
    runtime = (time_after - time_before) * 1000000
    
    # Results found
    if (data):
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
        
def GuiHashRange():
    """
    Retrieve records with a given range when database type is hash.
    Just a proof of concept, doesn't return anything readable or write to the
    answer file yet, but it does work.
    """
    # Take input values
    msg = "Please enter the range search key values."
    title = "Ranged Search"
    fieldNames = ["Lower Bound", "Upper Bound"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    if fieldValues == None:
        eg.msgbox('Operation cancelled')
        return

    lowerKey = fieldValues[0]
    upperKey = fieldValues[1]

    # Check that lower key < upper key.
    if upperKey <= lowerKey:
        eg.msgbox("Error! Upper bound must be larger than lower bound.")
        return
        
    # Change the key from string to bytes:
    lowbyte_key = lowerKey.encode('utf-8')
    upperbyte_key = upperKey.encode('utf-8')

    current = cur.first()

    # Iterate through the database, taking time before and after
    resultlist = []
    i = 0
    time_before = time.time()
    while i < len(DATABASE):
        if lowbyte_key <= current[0] <= upperbyte_key:
            resultlist.append((current[0], current[1]))
        current = cur.next()
        i += 1

    time_after = time.time()
    # Get time in microseconds
    runtime = (time_after - time_before) * 1000000
    
    # Results found
    if (resultlist):
        for item in resultlist:
            answers.write(item[0].decode('utf-8'))
            answers.write('\n')
            answers.write(item[1].decode('utf-8'))
            answers.write('\n')
            answers.write('\n')
    else:
        text = ("No results found for the following key range:\n{}\n{}\nTime: {} microseconds".format(lowerKey, upperKey, runtime))

    msg = "Results:" 
    title = "Retrieve With Key"
    eg.textbox(msg, title, "Number of records: {} in {} microseconds\n{}".format(len(resultlist), runtime, resultlist))
        

def GuiRetrieveWithData():
    """
    Retrieve records with a given data
    """
    msg = "Please enter the data you would like to search for"
    title = "Retrieve key with given data"
    searchdata = eg.enterbox(msg, title)

    if searchdata == None:
        eg.msgbox("Operation cancelled.")
        return


    # Change the data from string to bytes:
    bytes_data = searchdata.encode('utf-8')

    time_before = time.time()
    
    first = cur.first()
    data = first[1]

    i = 1 
    while data != bytes_data and i < len(DATABASE):
        next_record = cur.next()
        data = next_record[1]

        i += 1

    if data == bytes_data:
        key = next_record[0]
    else: 
        key = 0
    
    time_after = time.time()

    # Get time in microseconds
    runtime = (time_after - time_before) * 1000000

    # Results found
    if (key):
        # Open answers file.
        answers = open('answers','a')
        # Convert from bytes to a string.
        key = key.decode('utf-8')
        # Append to answers file.
        answers.write(key)
        answers.write('\n')
        answers.write(searchdata)
        answers.write('\n')
        answers.write('\n')
        text = ("Data input: \n{} \nKey value found: \n{} \nNumber of records retrieved: 1 \nTime: {} microseconds.".format(searchdata, key, runtime))
    # No results
    else:
        text = ("No results found for the following data: \n{} \nNumber of records retrieved: 0 \nTime: {} microseconds".format(searchdata, runtime))

    msg = "Results:" 
    title = "Retrieve With Data"
    eg.textbox(msg, title, text)


def GuiRetrieveWithRange():
    """
    Retrieve records with a given range of key values
    """
    msg = "Please enter the range search key values."
    title = "Ranged Search"
    fieldNames = ["Lower Bound", "Upper Bound"]
    fieldValues = []
    fieldValues = eg.multenterbox(msg, title, fieldNames)
    if fieldValues == None:
        eg.msgbox('Operation cancelled')
        return

    lowerKey = fieldValues[0]
    upperKey = fieldValues[1]

    # Check that lower key < upper key.
    if upperKey <= lowerKey:
        eg.msgbox("Error! Upper bound must be larger than lower bound.")
        return

    print("Lower Key: ",lowerKey)
    print("Upper Key: ",upperKey)
    
    time_before = time.time()
    # Get the next key that is greater than lowerKey or equal to it.
    # cur.set_range returns the key,data pair. Key is at 0th index.
    tempPair = (cur.set_range(lowerKey.encode('utf-8')))
    # Check if there are no results
    if (tempPair == None):
        time_after = time.time()
        # Get the runtime in microseconds
        runtime = (time_after - time_before) * 1000000
        text = ("No results found in the following range: \nLower Bound: {}  \nUpper Bound: {} \nNumber of records retrieved: 0 \nTime: {} microseconds".format(lowerKey, upperKey, runtime))
    else:
        tempKey = tempPair[0]
        tempData = tempPair[1]
        tempKey = tempKey.decode('utf-8')
        tempData = tempData.decode('utf-8')
        # Create a list to hold all keys found by range search
        rangeResults = []
        # Continue getting keys until 1 is larger than the upperKey.
        while tempKey <= upperKey:
            # Add to results
            rangeResults.append((tempKey, tempData))
            # Append to answers file.
            answers.write(tempKey)
            answers.write('\n')
            answers.write(tempData)
            answers.write('\n')
            answers.write('\n')
            # Get the next pair.
            tempPair = (cur.next())
            tempKey = tempPair[0]
            tempData = tempPair[1]
            tempKey = tempKey.decode('utf-8')
            tempData = tempData.decode('utf-8')
            
        time_after = time.time()
        # Get the runtime in microseconds
        runtime = (time_after - time_before) * 1000000
        numResults = len(rangeResults)
        text = ("Data input: \nLower Bound: {} \nUpper Bound: {} \nNumber of records retrieved: {} \nTime: {} microseconds \nRecords found: \n{}".format(lowerKey, upperKey, numResults, runtime, rangeResults))

    msg = "Results:" 
    title = "Retrieve With Data"
    eg.textbox(msg, title, text)
    return 

def GuiDestroyDatabase():
    """
    Destroy the database
    """
    # Close the existing database handle.
    DATABASE.close()
    try:
        SEC_DB.close()
    except:
        pass
    # Open a new database handle and drop the database.
    db_destroy = db.DB()
    if "indexfile" in sys.argv: sec_destroy = db.DB()
    try:
        db_destroy.remove(DB_FILE)
        if "indexfile" in sys.argv: sec_destroy.remove(SDB_FILE)
        eg.msgbox("Database was successfully dropped.")
        db_destroy.close()
    except Exception as e:
        eg.msgbox("Database has already been dropped")

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
    DATABASE.open(DB_FILE)
    eg.msgbox("Existing database found, opening existing database")
    database_exists = True
    cur = DATABASE.cursor()
except:
    eg.msgbox("No existing database found. Be sure to create a new one.")
    database_exists = False

try:
    SEC_DB = db.DB()
    SEC_DB.open(SDB_FILE)
    sec_cur = SEC_DB.cursor()
except:
    pass

# Open answers file.
answers = open('answers','w')

while True:
    msg = "CMPUT 291 Project 2, by Victoria Bobey, Sarah Morris, and Eldon Lake"
    title = "mydbtest"
    choices = ["Create and populate the database",
               "Retrieve records with a given key",
               "Retrieve records with a given data",
               "Retrieve records with a given range of key values",
               "Destroy the database",
               "Grab a random key for testing"]
    choice = eg.choicebox(msg, title, choices)
    if choice == choices[0]:
        if not database_exists:
            GuiCreateDatabase()
            # These lines moved here because python scoping was misbehaving
            DATABASE = db.DB()
            DATABASE.open(DB_FILE)
            cur = DATABASE.cursor()
            if "indexfile" in sys.argv:
                SEC_DB = db.DB()
                SEC_DB.open(SDB_FILE)
                sec_cur = SEC_DB.cursor()
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
            if "indexfile" in sys.argv or "IndexFile" in sys.argv:
                GuiIndexData()
            else:
                GuiRetrieveWithData() 
        else:
            eg.msgbox("Error! Must create database first.")
    elif choice == choices[3]:
        if database_exists:
            if "HASH" in sys.argv or "hash" in sys.argv:
                GuiHashRange()
            else:
                GuiRetrieveWithRange()
        else:
            eg.msgbox("Error! Must create database first.")
    elif choice == choices[4]:
        if database_exists:
            GuiDestroyDatabase()
            database_exists = False
        else:
            eg.msgbox("Error! Must create database first.")
    elif choice == choices[5]:
        eg.textbox("Key: ", "Random Key", Testing(1))

    msg = "Do you want to continue?"
    title = "Continue?"
    if eg.ccbox(msg, title, ('Continue', 'Exit')): # Continue/Cancel dialog
        pass # user chose Continue
    else:
        answers.close()
        GuiDestroyDatabase()
        sys.exit(0) # user chose Cancel

