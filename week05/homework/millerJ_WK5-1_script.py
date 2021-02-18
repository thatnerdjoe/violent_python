from binascii import hexlify
import os
import sys
import re

SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'Assignment 7 - URI and Email Regex'
SCRIPT_DATE = '2021-02-17'

'''
PROMPT:
    An excerpt of a memory dump extracted by Access Data's
    FTK Imager (memdump.bin or test.bin) has been provided.

        1) Copy the memory dump to the virtual desktop
            environment persistent storage area.

        2) Develop a python script and regular expressions
            to extract and report ALL the e-mail and urls
            found in the memory dump.

    REGULAR EXPRESSIONS HELP

    ePatt = re.compile(b'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
    uPatt = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*')

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

###
# CLASSES
###


class blank():
    pass


###
# MAIN SCRIPT
###

# list of files in `directory`
emailList = []
uriList = []

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

ePatt = re.compile(b'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}')
uPatt = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*')


try:
    print(f'\nSearching for URIs and email addresses in {filePath}...\n')
    separator(promptLen)
    with open(filePath, 'rb') as binaryFile:
        while True:
            # create a chunk of len CHUNK_SIZE
            chunk = binaryFile.read(CHUNK_SIZE)
            if chunk:
                # Create list of email addresses found in chunk
                emails = ePatt.findall(chunk)
                # Create list of URIs found in chunk
                uri = uPatt.findall(chunk)

                # Iterate over each list and add to their respective lists
                for eachEmail in emails:
                    emailList.append(eachEmail.decode())
                for eachURI in uri:
                    uriList.append(eachURI.decode())
            else:
                break

    # Print the email address
    print('\tEmail addresses within file:\n')
    if (len(emailList) < 1):
        print("No email addresses found.")
    else:
        for each in emailList:
            print(each)

    separator(promptLen)

    # Print the URIs
    print('\tURIs found within file:\n')
    if (len(uriList) < 1):
        print('No URIs found.')
    else:
        for each in uriList:
            print(each)

except:
    print('\nERROR: Could not open file!\nEnsure proper read permissions exist.\n')
