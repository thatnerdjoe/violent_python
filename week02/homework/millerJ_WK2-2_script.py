from __future__ import print_function
import hashlib
import os

'''
Week Two Assignment 2-2 - File Hashing

Author:     Joseph Miller
Date:       Jan 21, 2021
Assignment: #2-2
'''
SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_DATE = 'Jan 27, 2021'
SCRIPT_NAME = 'Assignment #2-2: Log Parser'
'''
Complete the script below to do the following:
1) Add your name, date, assignment number to the top of this script
2) Using the os library and the os.walk() method 
   a) Create a list of all files
   b) Create an empty dictionary named fileHashes 
   c) Iterate through the list of files and
      - calculate the md5 hash of each file
      - create a dictionary entry where:
        key   = md5 hash
        value = filepath
    d) Tterate through the dictionary
       - print out each key, value pair
    
3) Submit
   NamingConvention: lastNameFirstInitial_Assignment_.ext
   for example:  hosmerC_WK1_script.py
                 hosmerC_WK1_screenshot.jpg
   A) Screenshot of the results in WingIDE
   B) Your Script
'''

def HashFile(filePath):
   try:
      with open(filePath, 'rb') as fileToHash:
         fileContents = fileToHash.read()
         hashObj = hashlib.md5()
         hashObj.update(fileContents)
         digest = hashObj.hexdigest()
         return digest
   except Exception as err: 
      return str(err)

directory = "."

fileList = []
fileHashes = {}

for root, dirs, files in os.walk(directory):

    # Walk the path from top to bottom.
    # For each file obtain the filename

   for fileName in files:
      path = os.path.join(root, fileName)
      fullPath = os.path.abspath(path)
      fileList.append(fileName)

# For each item listed in the path
# call HashFile() to generate hash
# and store in fileHashes{} 

for eachItem in fileList:
    fileHash = HashFile(eachItem)
    fileHashes.update({eachItem:fileHash})

print('\n'+SCRIPT_AUTHOR)
print(SCRIPT_DATE)
print(SCRIPT_NAME)
print(f'\nMD5 Hashes for files in {os.getcwd()}:', end='\n\n')

for eachKey in fileHashes:
   print(f'{eachKey}: {fileHashes.get(eachKey)}',)

print()