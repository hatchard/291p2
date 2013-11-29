291p2
=====

Project 2 for CMPUT 291

Run: python3  mydbtest.py db_type_option, Note: For now, just go python3 mydbtest.py
I only have btrees working atm. Hash is easy, just change db.DB_BTREE on line 42 to db.DB_HASH

Things to complete:
1) Create and populate a database (DONE)

Queries: 
For all the queries, the program must display the number of records retrieved and the total execution time in micro seconds.
All records (key/data pairs) retrieved must be appended into a file named "answers" in the local directory. 
The file must be in the format that each record occupies three lines: one line for the key string, followed by one line for the data string and one line for an empty string.
2) Retrieve records with a given key (DONE)
3) Retrieve records with given data (DONE)
*4) Retrieve records with a given range (IMPLEMENTED BUT NEEDS ANSWER THING)
5) Destroy database (DONE)
6) GUI (DONE)
*7) Create IndexFile type, which I believe is a B+tree
*8) Perform tests and put results in a table
*9) Report
*10) Makefile
