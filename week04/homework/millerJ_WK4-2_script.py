from prettytable import PrettyTable
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import sys

'''
PROMPT:
    Expand the script as follows:

        1) Allow the user to enter a path to a directory containing jpeg files.

        2) Using that path, process only the .jpg files contained in that folder
            (use the testimages.zip set of images)

        3) Extract, EXIF data from each of the images and create a pretty table output
            NOTE: your script can extract other EXIF data that you find interesting

        4) Finally, you will Plot the geolocation of each image on a map.

    NOTE: There are several ways to do this, however, the easiest method would be to use
    the MapMaker App, at https://mapmakerapp.com/. You can either manually enter the
    lat/lon values your script generates or you can place your results in a CSV file
    and upload the data to the map.
'''
###
# Script Header
###

SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'Assignment 4 - EXIF Data & Processing'
SCRIPT_DATE = '2021-02-10'


###
# Constants
###

JPG_EXTENSIONS = ['.jpg', ',jpeg', '.JPEG', '.JPG']

###
# Functions
###


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


def verifyAndProcessJPG(fPath, fName):
    '''
    '''
    absPath = os.path.join(fPath, fName)
    fileExt = os.path.splitext(absPath)[1]
    isJPG = True if fileExt in JPG_EXTENSIONS else False
    if isJPG:
        return ProcessedJPG(absPath, fileExt)


###
# Classes
###

class ExifKeyList():

    def __init__(self):
        ###
        # EXIF Key-Values
        ###
        # creat lists of the TAGS dict's keys and values
        self.exifKeys = list(TAGS.keys())
        self.exifValues = list(TAGS.values())

        # create dict to store Key-Value pairs of desired ExifTags.TAGS keys
        self.exifKeyList = {'DateTimeOriginal': None,
                            'Make': None,
                            'Model': None,
                            'GPSInfo': None}

        # The list of keys and values should be aligned
        # and should therefore have an identical index
        for each in self.exifKeyList:
            # key becomes index of specified tag in gpsKeyList
            index = self.exifValues.index(each)
            # Add the matching key to the gpsKeyList
            self.exifKeyList.update({each: self.exifKeys[index]})
        ###
        # GPS Key-Values
        ###
        #
        self.gpsKeys = list(GPSTAGS.keys())
        self.gpsValues = list(GPSTAGS.values())

        # create dict to store Key-Value pairs of desired ExifTags.GPSTAGS keys
        self.gpsKeyList = {'GPSLatitude': None,
                           'GPSLongitude': None,
                           }

        # The list of keys and values should be aligned
        # and should therefore have an identical index
        for each in self.gpsKeyList:
            # key becomes index of specified tag in gpsKeyList
            index = self.gpsValues.index(each)
            # Add the matching key to the gpsKeyList
            self.gpsKeyList.update({each: self.gpsKeys[index]})

        # 'GPSInfo is not in GPSTAGS, add after populating
        self.gpsKeyList.update({'GPSInfo': self.GetExifKeys('GPSInfo')})

    def GetExifKeys(self, key):
        return self.exifKeyList.get(key)

    def GetGpsKeys(self, key):
        return self.gpsKeyList.get(key)


class ProcessedJPG():

    def __init__(self, absPath, fileExt):
        self.absPath = absPath
        self.fileExt = fileExt
        self._isValid = False
        self.imgTimeStamp = None
        self.imgCameraModel = None
        self.imgCameraMake = None
        self.imgGPS = {'latitude': None,
                       'longitude': None}

        # attempt opening image with PIL
        try:
            IMG = Image.open(absPath)
            self._isValid = True
            exif = IMG._getexif()
            if exif:
                self.SetImageExif(exif)
                self.SetImageGPS(exif)
            else:
                self.SetImageExif(None)
        # file is not a valid JPEG image
        except:
            self.SetImageExif(None)

    def ConvertCoords(self, lat, lon):

    def GenerateListRow(self):
        '''
        Returns a list containing image metadata of a file
        '''
        return [self.absPath, self.imgTimeStamp, self.imgCameraModel,
                self.imgCameraMake, self.imgGPS['latitude'], self.imgGPS['longitude']]

    def SetImageExif(self, exif):
        '''
        Getter method for populating image metadata: "Image Timestamp",
        "Camera Make", and "Camera Model", if possible.
        '''
        timestampKey = keyList.GetExifKeys('DateTimeOriginal')
        makeKey = keyList.GetExifKeys('Make')
        modelKey = keyList.GetExifKeys('Model')

        self.imgTimeStamp = exif.get(timestampKey) if exif else 'N/A'
        self.imgCameraMake = exif.get(makeKey) if exif else 'N/A'
        self.imgCameraModel = exif.get(modelKey) if exif else 'N/A'

    def SetImageGPS(self, exif):
        '''
        Getter method for populating image metadata: "GPS Lat." and "GPS Long.", if possible.
        '''
        gpsIndex = keyList.GetGpsKeys('GPSInfo')
        latIndex = keyList.GetGpsKeys('GPSLatitude')
        longIndex = keyList.GetGpsKeys('GPSLongitude')

        gpsInfo = exif.get(gpsIndex)

        if gpsInfo:

        self.imgGPS.update(
            {'latitude': gpsInfo[latIndex] if exif else 'N/A'})
        self.imgGPS.update(
            {'longitude': gpsInfo[longIndex] if exif else 'N/A'})


###
# Script begin!
###

# Initialize and declare variables and objects
keyList = ExifKeyList()

# Output table
table = PrettyTable(
    ['File', 'Timestamp', 'Camera Make', 'Camera Model', 'GPS Lat.', 'GPS Long.'])

# list of files in user-specified var `directory`
fileNames = []

# list of objects referring to file metadata in user-specified var `directory`
processedImages = []

# Prompt for user
prompt = 'Please, enter a directory:'
promptLen = len(prompt)

# Print header
separator(promptLen)
print('\n' + SCRIPT_AUTHOR + '\n' + SCRIPT_NAME +
      '\n' + SCRIPT_DATE, end='\n\n')

# Prompt for user input
separator(promptLen)
directory = input(prompt + ' ')
separator(promptLen)

try:
    fileNames = os.listdir(directory)

    for eachFile in fileNames:
        path = os.path.abspath(directory)
        IMG = verifyAndProcessJPG(path, eachFile)
        if IMG:
            print(IMG.GenerateListRow())
        else:
            continue

    # for each in processedImages:
    #     print(each)
    # # for eachFile in processedFiles:
    # #     table.add_row(eachFile.GenerateListRow())

    # for each in processedImages:
    #     print(each)
    # print('NOTICE: Images without proper read-permissions will not have metadata')

except (NotADirectoryError, FileNotFoundError) as e:
    print("No such directory.")
