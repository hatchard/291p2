# Create a b-tree database. Uses bsddb3 
# DB_SIZE is set to 3 for testing purposes. Change to 100000 later.

from bsddb3 import db
from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')

# Not sure if it needs to be in this directory,
# Just went with the example for now
DB_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 3  # Change to 100000 later
SEED = 10000000

def key_record(key, cur):
    """
    Retrieve a record with a given key.
    Input key should be a string, which gets encoded to bytes.
    Returns <key,data> pair is exists.
    Returns None if key does not exist.
    """
    # Change key from string to bytes
    strkey = key.encode('utf-8')
    data = cur.set(strkey)
    if (data):
        print("Number of records retrieved: 1   Time: ", "time goes here")
        print(data)
        return(data)
    else:
        print (key, "was not found.")
        return (None)

def main ():

    # Check if there is an existing database
    try:
        print ("Openning existing database.")
        DATABASE = db.DB()
        DATABASE.open("sample_db")
    except:
        DATABASE = db.DB()
        # Create a hash database 
        print ("Database doesn't exist. Creating a new one.")
        DATABASE.open("sample_db", None, db.DB_BTREE, db.DB_CREATE)

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
    """
    # Fetch all data from the database and print it (testing)
    print (" ")
    print ("Printing all data.")
    iter = cur.first()
    while iter:
        print(iter)
        iter = cur.next()
    """
    # Testing some functions here.
    print(" >>>      TESTING      <<<")
    print("Get a record from a given key:")
    # Just used the last added key (as a string) here.
    key_record(key.decode('utf-8'), cur)
    print("Try to get a record from a key that does not exist:")
    key_record("abc", cur)

    # Close the database
    try:
        cur.close()
        DATABASE.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

