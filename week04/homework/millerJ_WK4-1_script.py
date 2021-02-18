from prettytable import PrettyTable
from PIL import Image
import os
import sys
import time

SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'Assignment 5 - Image Searching'
SCRIPT_DATE = '2021-02-10'

'''
PROMPT:
    Extract the testimages provided into the Virtual
    Desktop Environment (in the persistent storage areas)

    Develop a script that:

        1) Prompts the user for a directory path to search

        2) Verify that the path provided exists and is a
            directory

        3) Iterate through each file in that directory and
            examine it using PIL.

        4) Generate a prettytable report of your search
            results (sample shown here)

        +---------------------------------------+-
        | File                  | Ext  | Format | Width | Height | Mode |
        +---------------------------------------+------+--------+-------+
        | .\photos\PH01236U.BMP | .BMP | BMP    | 216    | 143   | P |
        | .\photos\PH02039U.BMP | .BMP | BMP    | 216    | 143   | P |
        | .\photos\PH02752U.BMP | .BMP | BMP    | 216    | 142   | P |
        | .\photos\38467giu.gif | .gif | GIF    | 300    | 212   | P |
        | .\photos\AG00004_.GIF | .GIF | GIF    | 140    | 135   | P |

    Submit:

        1) Your Python script

        2) A screenshot of the successful execution and output
'''


def separator(l):
    '''
    Line break made from '=' characters
    '''
    for x in range(l):
        print('=', end='')
    print()


def printTable(t):
    '''
    Callable function to print the PrettyTable obj
    with various formatting args
    '''
    t.align = 'l'
    t.align["Size"] = 'r'
    print(t.get_string())


class ProcessedImg():

    def __init__(self, fPath, fName):
        self.fileName = fName
        self.filePath = fPath
        # create string holding full file path
        self.absPath = os.path.join(self.filePath, self.fileName)
        # returns True unless file is invalid sym-link
        self._isValid = os.path.exists(self.absPath)
        # placeholder flag if object refers to an image
        self._isImage = False
        # if the file is valid, try to process image metadata
        if self._isValid:
            # get the filesize as string in form '### B'
            self.fileSize = str(os.path.getsize(self.absPath)
                                ) + ' B'
            # get the file extension
            self.fileExt = os.path.splitext(
                self.absPath)[1]

            try:  # attempt opening image with PIL
                with Image.open(self.absPath) as img:
                    self._isImage = True
                    # populate attr with image metadata
                    self._SetImageDetails(img)
            # file is not a recognizable image
            except:
                self._SetImageDetails(None)
        # if file is invalid sym-link, populate metadata accordingly
        else:
            self._SetImageDetails(None)
            self.fileExt = 'Invalid sym-link'
            self.fileSize = 'N/A'

    def GenerateListRow(self):
        '''
        Returns a list containing image metadata of a file: "Extension",
        "Image Format", "Width", "Height", and "Mode"
        '''
        # check is file is a directory, set file extension to reflect this
        fileExt = 'Dir' if os.path.isdir(self.absPath) else self.fileExt
        # Print only the file name and extension
        fileName = os.path.basename(self.absPath)

        return [self._isImage, fileName, self.fileSize, fileExt,
                self.imgFormat, self.imgWidth, self.imgHeight, self.imgMode]

    def _SetImageDetails(self, img):
        '''
        Setter method for populating image metadata: "Image Format",
        "Width", "Height", and "Mode", if possible.
        '''
        self.imgFormat = img.format if img else 'N/A'
        self.imgWidth = img.width if img else 'N/A'
        self.imgHeight = img.height if img else 'N/A'
        self.imgMode = img.mode if img else 'N/A'

###
# Script begin!
###


# Initialize and declare variables and objects
# Output table
table = PrettyTable(
    ['Image?', 'File', 'Size', 'Ext', 'Fmt', 'Width', 'Height', 'Mode'])

# list of files in `directory`
fileNames = []

# Prompt for user
prompt = 'Please, enter a directory:'
promptLen = len(prompt)

# Print header
separator(promptLen)
print('\n' + SCRIPT_AUTHOR + '\n' + SCRIPT_NAME + '\n' + SCRIPT_DATE, end='\n\n')

# Prompt for user input
separator(promptLen)
directory = input(prompt + ' ')
separator(promptLen)

try:
    fileNames = os.listdir(directory)
    # Print the specified directory and omit from table to save horizontal space
    print('Processing JPEG files in:\n   ' + os.path.abspath(directory))
    separator(promptLen)
    # iterate through each file in `directory` and process accordingly
    for eachFile in fileNames:
        path = os.path.abspath(directory)
        IMG = ProcessedImg(fPath=path, fName=eachFile)
        # append each row to table in-place to save memory
        if IMG:
            table.add_row(IMG.GenerateListRow())

    printTable(table)
    print('NOTICE: Images without proper read-permissions will not have metadata', end='\n\n')

except (NotADirectoryError, FileNotFoundError) as e:
    print(e)
