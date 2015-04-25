__author__ = 'VerDe'
'''
Features:
- Accept input from user and inserts it into a local database
- Read from the local database
'''

import sqlite3


#  Accepts input from the user and manipulates it.
#  The input will be inserted in the sqlite db through the insert_entry function
def write_entry():
    writing = True
    entry = ""
    print("What's on your mind?\nTip: type 'done' to finish writing the entry.\n")
    while writing:
        entry_row = input()
        if entry_row.lower() == "done":
            print()
            writing = False
        else:
            entry += entry_row + "\n"
    if entry != "":
        return entry


#  Accepts input from the user and checks to see if the selected entry id exists in the database
#  Returns the id if valid.
#  ID is passed to the get_entry function
def choose_entry():
        conn = sqlite3.connect("Journal.db")
        cur = conn.cursor()
        entry_list = []
        done = False
        while not done:
            try:
                cur.execute('''SELECT ID, EntryDate FROM Entries''')
            except sqlite3.OperationalError:
                print("You have no entries yet.\n")
                break

            print("Entry list:")
            for row in cur.fetchall():
                print("{0}    {1}".format(row[0], row[1]), end="")
                if str(row[0]) not in entry_list:
                    entry_list.append(str(row[0]))
                print()
            user_pick = input("Choose an entry, or type 'done': ")
            if user_pick == "done":
                break
            else:
                if str(user_pick) not in entry_list:
                    print("Not a valid entry.\n")
                    continue
                else:
                    print()
                    conn.close()
                    done = True
                    return user_pick


#  Returns chosen entry from the local database
def get_entry(s):
    conn = sqlite3.connect("Journal.db")
    cur = conn.cursor()
    try:
        cur.execute('''SELECT Entry FROM Entries WHERE ID = ?;''', (str(s),))
        row = cur.fetchone()
        if row:
            output_entry = row[0]
            print(output_entry)
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
running = True
while running:
    mode = input("Do you wish to read or write?\nTip: type 'quit' to quit.\n")
    if mode.lower() == "read":
        chosen_entry = choose_entry()
        if chosen_entry:
            get_entry(chosen_entry)
        continue
    if mode.lower() == "write":
        written_entry = write_entry()
        if written_entry:
            insert_entry(written_entry)
        continue
    if mode.lower() == "quit":
        running = False
    else:
        print("Invalid input. Accepted values are 'read', 'write' or 'quit'\n")