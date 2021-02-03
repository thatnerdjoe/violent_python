from __future__ import print_function
import time
import sys
import os
from binascii import hexlify

SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'Assignment 4 - File Processing'
SCRIPT_DATE = '2021-02-03'

'''
Week Two Assignment 4 - File Processing Object

Complete the script below to do the following:
1) Add your name, date, assignment number to the top of this script
2) Create a class named FileProcessor
   a) The Init method shall:
      i) verify the file exists
      ii) Extract key file system metadata from the file
          and store them as instance attribute
          i.e. FilePath, FileSize, MAC Times, Owner, Mode etc.
   b) Create a GetFileHeader Method which will
      i) Extract the first 20 bytes of the header
         and store them in an instance attribute
   c) Create a PrintFileDetails Method which will
      i) Print the metadata
      ii) Print the hex representation of the header

3) Demonstrate the use of the new class
   a) prompt the user for a directory path
   b) using the os.listdir() method extract the filenames from the directory path
   c) Loop through each filename and instantiate and object using the FileProcessor Class
   d) Using the object
      i) invoke the GetFileHeader Method
      ii) invoke the PrintFileDetails Method

4) Submit
   NamingConvention: lastNameFirstInitial_Assignment_.ext
   for example:  hosmerC_WK3_script.py
                 hosmerC_WK3_screenshot.jpg
   A) Screenshot of the results in WingIDE
   B) Your Script
'''


class FileProcessor:
    '''
    Contains methods and attributes related to file metadata.
    '''

    def __init__(self, fPath, fName):
        self.fileName = fName
        self.absPath = fPath
        self.filePath = os.path.join(self.absPath, self.fileName)
        self._isValid = os.path.exists(self.filePath)
        self.fileHeader = ''
        # self.metadata = {'File Size': '',
        #                  'Modified Time': '',
        #                  'Create Time': '',
        #                  'Owner UID': '',
        #                  }
        if self._isValid:
            stats = os.stat(self.filePath)
            self.metadata = {'File Size': str(stats.st_size) + " bytes",
                             'Modified Time': time.ctime(stats.st_mtime),
                             'Create Time': time.ctime(stats.st_atime),
                             'Owner UID': stats.st_uid,
                             }

    def GetFileHeader(self):
        '''
        Sets FileHeader attribute to the first 20 bytes of file as a hex-encoded string
        '''
        if self._isValid:
            '''
            Try to get file header info if file is valid
            '''
            try:
                with open(self.filePath, 'rb') as binFile:
                    self.fileHeader = hexlify(binFile.read(20))
            except IsADirectoryError:
                self.fileHeader = "Entity is a directory!"
            except:
                self.fileHeader = "Error opening file. Check file permissions."
        else:
            print(f'"{self.filePath}" is not a valid file/directory!')

    def PrintFileDetails(self):
        '''
        Outputs the metadata of a file: "Date Created", "Date Modified",
        "File Size", and "File Header"
        '''
        if self._isValid:
            for item in self.metadata:
                print(f'{item}: {self.metadata[item]}')
            print(f'File Header: {self.fileHeader}', end='\n\n')
        else:
            print("NOTICE: symbolic link may be invalid", end='\n\n')


def separator():
    '''
    Line break made from '=' characters
    '''
    for x in range(60):
        print('=', end='')
    print()


fileNames = []
processedFiles = []

print('\n' + SCRIPT_AUTHOR + '\n' + SCRIPT_NAME + '\n' + SCRIPT_DATE, end='\n\n')

separator()
directory = input('Please, enter a directory: ')
separator()

try:
    fileNames = os.listdir(directory)
    for eachFile in fileNames:
        path = os.path.abspath(directory)
        processedFiles.append(FileProcessor(fPath=path, fName=eachFile))
except:
    print("No such directory.")

for eachItem in processedFiles:
    print('File: ' + eachItem.filePath)
    eachItem.GetFileHeader()
    eachItem.PrintFileDetails()

separator()
