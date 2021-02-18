from binascii import hexlify
from operator import attrgetter
from prettytable import PrettyTable
import os
import sys
import re

SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'Assignment 8 - Unique String Sorting'
SCRIPT_DATE = '2021-02-17'

'''
PROMPT:
    An excerpt of a memory dump extracted by Access Data's FTK Imager
    (memdump.bin or test.bin) has been provided.

        1) Copy the memory dump to the virtual desktop
            environment persistent storage area.

        2) Develop a Python script to process the memory
            dump and identify unique strings of 5-12 characters along
            with the number of occurrences of each unique string.
            Then display the resulting list of strings and occurrences
            in a prettytable sorted by the highest number of occurrences.

    REGULAR EXPRESSION HELP

        word regx (more specifically continuous alpha string pattern)

        wPatt = re.compile(b'[a-zA-Z]{5,15}')

    Submit:

        1) Your Python script

        2) Screenshot of your results.
'''
###
# GLOBAL VARS
###

# Size of data chunks to read from a binary file.
# Too small of a value can truncate regex patterns, and
# too high of a value can quickly take up memory. Recommend 256.
CHUNK_SIZE = 256

###
# FUNCTIONS
###


def separator(l):
    '''
    Line break made from '=' characters
    '''
    for x in range(l):
        print('=', end='')
    print()


def printTable(table, file_desc=None):
    '''
    Callable function to print the PrettyTable obj
    with various formatting args. Will print table to
    file if passed a file descriptor.
    '''
    table.align = 'l'
    if (file_desc == None):
        print(table.get_string())
    else:
        file_desc.write(table.get_string())
        print(f'Wrote to file {file_desc.name}\n')

###
# CLASSES
###


class StringListIterator:
    '''
    Object blueprint for Iterator of StringList. Traverses 
    a linked-list.
    '''

    def __init__(self, head):
        self.current = head

    def __iter__(self):
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        else:
            item = self.current
            self.current = self.current.next_item
            return item


class StringList:
    '''
    Object blueprint for an iterable linked-list data structure. 
    Can only add items to this list. Any new items with a value
    already in the list will increment the count of its value. 
    '''

    def __init__(self):
        # Size of the list
        self.size = 0
        # Head of the list
        self.head = None
        # Tail of the list
        self.tail = None

    def __iter__(self):
        return StringListIterator(self.head)

    def addItem(self, word):
        # Flag for logic control
        flag = 1
        # Increment the size of the list
        self.size += 1
        # Add new item to head if list is empty
        if (self.head == None):
            self.head = StringListItem(word)
            self.tail = self.head
        # Otherwise, search list for the string
        # and increment its count
        else:
            for each in self:
                if (word == each.value):
                    each.count += 1
                    # Set flag to 0 if match found
                    flag = 0
                    break

        # No match was found, add item to tail of list
        if (flag > 0):
            self.tail.next_item = StringListItem(word)
            self.tail = self.tail.next_item


class StringListItem:
    '''
    Object blueprint for nodes on the parent linked list. Contains fields
    for count, value, and pointer to next node.
    '''

    def __init__(self, word):
        # number of occurences a unique string was encountered
        self.count = 1
        # value of a unique string in a file
        self.value = word
        # pointer to next node
        self.next_item = None


###
# MAIN SCRIPT
###

# Create table object and create headers
OutTable = PrettyTable(['String Token', 'Occurrences'])


#  list of files in `directory`
StrList = StringList()

# Prompt for user
prompt = 'Please, enter the path of a binary file:'
promptLen = len(prompt)

# Print header
separator(promptLen)
print('\n' + SCRIPT_AUTHOR + '\n' + SCRIPT_NAME + '\n' + SCRIPT_DATE, end='\n\n')

# Prompt for user input
separator(promptLen)
filePath = input(prompt + ' ')
separator(promptLen)

# regex pattern for alphabetic strings 5 to 12 chars in length
wPatt = re.compile(b'[a-zA-Z]{5,12}')

try:
    print(f'Searching for strings in {filePath}...')
    with open(filePath, 'rb') as binaryFile:
        while True:
            # create a chunk of len CHUNK_SIZE
            chunk = binaryFile.read(CHUNK_SIZE)
            if chunk:
                # Create list of words found in chunk
                words = wPatt.findall(chunk)
                # Iterate over list and add to the linked-list obj
                for w in words:
                    StrList.addItem(w.decode())
            # if chunk is empty, break
            else:
                break
    # I wanted to merge-sort the linked-list in place for efficiency, but cannot complete
    # The rest of the implementation works fine, though.

    # Sort the linked-list obj based on 'count' and store resulting list
    temp_list = reversed(sorted(StrList, key=attrgetter('count')))
    # Iterate over sorted list and add it to the table
    for each in temp_list:
        OutTable.add_row([each.value, each.count])

    # Open a file for output
        file_desc = open('millerJ_WK5-2_out.txt', 'w+')
    # Print the table to file
    printTable(OutTable, file_desc)
    file_desc.close()

except:
    print('\nERROR: Could not open file!\nEnsure proper read permissions exist.\n')
