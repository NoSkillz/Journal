__author__ = 'VerDe'
'''
Features:
- Read from file - filter by date
- Write to file - insert date
'''
from datetime import datetime


def read_entry():
    f = open("journal.txt", "r")
    lines = f.readlines()
    f.close()
    entry_list = {}
    entry_count = 0
    for line in lines:
        if line.find("Entry date") == 0:
            entry_count += 1
            entry_list[str(entry_count)] = line
            # print(line, end="")
    print("Table of contents:")
    for k, v in entry_list.items():
        print(k, v, end="")
    selected_entry = input("Select an entry from the list: ")
    if selected_entry in entry_list.keys():
        for line in lines:
            print(line.find(entry_list[selected_entry]))
            # need to find the line and print until reaching *** END ENTRY ***


def write_entry():
    writing = True
    entry = ""
    # count = 0
    print("What's on your mind?\n")
    while writing:
        entry_row = input()
        if entry_row.lower() == "done":
            writing = False
        else:
            entry += entry_row + "\n"
    return "Entry date: {0} o'clock\n{1}".format(str(datetime.now())[:16], entry)


def insert_entry(s):
    file = open("journal.txt", "a")
    file.write("{0}\n*** END ENTRY ***\n\n".format(s))
    file.close()


done = False
while not done:
    mode = input("Do you wish to read or write?")
    if mode.lower() == "read":
        read_entry()
        continue
    if mode.lower() == "write":
        # print(write_entry())
        insert_entry(write_entry())
        continue
    if mode.lower() == "quit":
        done = True
    else:
        print("Invalid input. Accepted values are 'read', 'write' or 'quit'")