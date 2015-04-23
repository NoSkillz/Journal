__author__ = 'VerDe'
'''
Features:
- Read from file - filter by date
- Write to file - insert date
'''
from datetime import datetime
import sqlite3


def read_entry():   # find
    f = open("journal.txt", "r")
    lines = f.readlines()
    f.close()
    entry_list = {}
    entry_count = 0  # number of entries found. will be used as keys (string) in entry_list dictionary

    for line in lines:
        if line.find("Entry date") == 0:    # find the start of an entry
            entry_count += 1
            entry_list[str(entry_count)] = line  # add the Entry date lines in the entry_list dict, to be filtered later

    if entry_list:  # if dictionary not empty
        print("\nTable of contents:")
        for k, v in entry_list.items():  # print keys and values in entry_list as a TOC
            print(k, v, end="")
        print()
    else:
        print("There are no entries. Maybe you should write one...\n")
        return

    selected_entry = input("Select an entry from the list: ")  # prompt to pick a pick from entry_list
    if selected_entry in entry_list.keys():
        copy = False
        entry = "\n" + str(entry_list[selected_entry]) + "\n"
        s = entry_list[selected_entry]
        for line in lines:
            if line == s:
                copy = True
            elif line == "*** END ENTRY ***":
                copy = False
            elif copy:
                entry += line
    print(entry)


def write_entry():  # write line by line to a string, to be appended to file through insert_entry
    writing = True
    entry = ""
    print("What's on your mind?\nTip: type 'done' to finish writing the entry.\n")
    while writing:
        entry_row = input()
        if entry_row.lower() == "done":
            print()
            writing = False
        else:
            entry += entry_row
    if entry != "":
        return entry


def select_entry(s):
    conn = sqlite3.connect("Journal.db")
    cur = conn.cursor()
    try:
        cur.execute('''SELECT Entry FROM Entries WHERE ID=?;''', s)
        row = cur.fetchone()
        if row:
            print(row)
        else:
            print("Invalid entry.\n")
    except sqlite3.OperationalError:
        print("No entries yet. Maybe you should write one...\n")

    conn.close()


def insert_entry(s):    # writes a string collected by write_entry
    # file = open("journal.txt", "a")
    # file.write("{0}\n*** END ENTRY ***\n\n".format(s))
    # file.close()
    conn = sqlite3.connect('''Journal.db''')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Entries(
    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    EntryDate DATETIME NOT NULL DEFAULT(datetime('now', 'localtime')),
    Entry VARCHAR NOT NULL);''')
    cur.execute('''INSERT INTO Entries(Entry) VALUES(?);''', (s,))
    conn.commit()
    conn.close()


# main program starts here
# pick read / write mode, or quit
done = False
while not done:
    mode = input("Do you wish to read or write?\nTip: type 'quit' to quit.\n")
    if mode.lower() == "read":
        select_entry("1")
        # read_entry()
        continue
    if mode.lower() == "write":
        written_entry = write_entry()
        if written_entry:
            insert_entry(written_entry)
        continue
    if mode.lower() == "quit":
        done = True
    else:
        print("Invalid input. Accepted values are 'read', 'write' or 'quit'\n")