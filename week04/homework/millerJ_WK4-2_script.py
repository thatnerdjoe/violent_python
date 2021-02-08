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
    '''
    Class for parsing the PIL.ExifTags dictionaries 
    '''

    def __init__(self):
        ###################
        # EXIF Key-Values
        ###################
        # create lists of the TAGS dict's keys and values
        self.exifKeys = list(TAGS.keys())
        self.exifValues = list(TAGS.values())

        # create dict to store Key-Value pairs of desired ExifTags.TAGS keys
        # 'GPSInfo' is found within TAGS, and will be passed to `gpsKeyList`
        self.exifKeyList = {'DateTimeOriginal': None,
                            'Make': None,
                            'Model': None,
                            'GPSInfo': None}
        '''
        The list of keys and values should be aligned and should 
        therefore have an identical index. By finding the index of a
        Value in TAGS, the corresponding Key can be found
        '''
        for each in self.exifKeyList:
            # key becomes index of specified tag in gpsKeyList
            index = self.exifValues.index(each)
            # Add the matching key to the gpsKeyList
            self.exifKeyList.update({each: self.exifKeys[index]})

        ##################
        # GPS Key-Values
        ##################
        # create list of GPSTAGS dict keys and values
        self.gpsKeys = list(GPSTAGS.keys())
        self.gpsValues = list(GPSTAGS.values())

        # create dict to store Key-Value pairs of desired ExifTags.GPSTAGS keys
        self.gpsKeyList = {'GPSLatitude': None,
                           'GPSLatitudeRef': None,
                           'GPSLongitude': None,
                           'GPSLongitudeRef': None,
                           }
        '''
        The list of keys and values should be aligned and should 
        therefore have an identical index. By finding the index of a
        Value in GPSTAGS, the corresponding Key can be found
        '''
        for each in self.gpsKeyList:
            # becomes index of specified tag in gpsKeyList
            index = self.gpsValues.index(each)
            # Add the matching key to the gpsKeyList
            self.gpsKeyList.update({each: self.gpsKeys[index]})

        # 'GPSInfo' is not in GPSTAGS, called from `exifKeyList`
        self.gpsKeyList.update({'GPSInfo': self.GetExifKeys('GPSInfo')})

    def GetExifKeys(self, value):
        '''
        Returns the Exif TAGS key cooresponding to the specified value  
        '''
        return self.exifKeyList.get(value)

    def GetGpsKeys(self, value):
        '''
        Returns the Exif GPSTAGS key cooresponding to the specified value 
        '''
        return self.gpsKeyList.get(value)


class ProcessedJPG():
    '''
    Class for processing JPG files with PIL.Image and PIL.ExifTags. Holds
    various metadata fields, such as "Timestamp", and "Camera Make", along
    with the methods to extract these fields from Exif data.  
    '''

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
            # If valid EXIF, extract data
            if exif:
                self.ExtractImageExif(exif)
                self.ExtractImageGPS(exif)
            # Otherwise, metadata set to 'N/A'
            else:
                self.ExtractImageExif(None)
        # file is not a valid JPEG image, set metadata to 'N/A'
        except:
            self.ExtractImageExif(None)

    def ConvertCoords(self, lat, latRef, lon, lonRef):
        '''
        Converts GPS coordinates in form of Tuple (deg, min, sec) into 
        degrees
        '''
        degrees = lat[0] if lat[0] > 0 else 0
        minutes = lat[1] if lat[1] > 0 else 0
        seconds = lat[2] if lat[2] > 0 else 0
        latDecimal = float((degrees + (minutes/60) + (seconds)/(60*60)))
        if latRef == 'S':
            latDecimal = latDecimal*-1.0

        degrees = lon[0] if lat[0] > 0 else 0
        minutes = lon[1] if lat[1] > 0 else 0
        seconds = lon[2] if lat[2] > 0 else 0
        lonDecimal = float((degrees + (minutes/60) + (seconds)/(60*60)))
        if lonRef == 'W':
            lonDecimal = lonDecimal*-1.0

        return [latDecimal, lonDecimal]

    def GenerateListRow(self):
        '''
        Returns a list containing image metadata of a file
        '''
        if None in self.imgGPS.values():
            lat = 'N/A'
            lon = 'N/A'
        else:
            lat = format(self.imgGPS['latitude'], '.03f')
            lon = format(self.imgGPS['longitude'], '.03f')

        fileName = os.path.basename(self.absPath)

        return [fileName, self.imgTimeStamp, self.imgCameraModel,
                self.imgCameraMake, lat, lon]

    def ExtractImageExif(self, exif):
        '''
        Getter method for populating image metadata: "Image Timestamp",
        "Camera Make", and "Camera Model", if possible.
        '''
        timestampKey = KeyList.GetExifKeys('DateTimeOriginal')
        makeKey = KeyList.GetExifKeys('Make')
        modelKey = KeyList.GetExifKeys('Model')

        self.imgTimeStamp = exif.get(timestampKey) if exif else 'N/A'
        self.imgCameraMake = exif.get(makeKey) if exif else 'N/A'
        self.imgCameraModel = exif.get(modelKey) if exif else 'N/A'

    def ExtractImageGPS(self, exif):
        '''
        Getter method for populating image metadata: "GPS Lat." and "GPS Long.", if possible.
        '''
        gpsIndex = KeyList.GetGpsKeys('GPSInfo')
        # Get Latitude and LatitudeRef GPSTAGS keys
        latIndex = KeyList.GetGpsKeys('GPSLatitude')
        latRefIndex = KeyList.GetGpsKeys('GPSLatitudeRef')
        # Get Longitude and LongitudeRef GPSTAGS keys
        lonIndex = KeyList.GetGpsKeys('GPSLongitude')
        lonRefIndex = KeyList.GetGpsKeys('GPSLongitudeRef')

        try:
            gpsInfo = exif.get(gpsIndex)
            vals = self.ConvertCoords(gpsInfo[latIndex],
                                      gpsInfo[latRefIndex],
                                      gpsInfo[lonIndex],
                                      gpsInfo[lonRefIndex])
        except:
            vals = None

        self.imgGPS.update(
            {'latitude': vals[0] if vals else None})
        self.imgGPS.update(
            {'longitude': vals[1] if vals else None})

###
# Script begin!
###


# Initialize and declare variables and objects
KeyList = ExifKeyList()

# Output table
table = PrettyTable(
    ['File', 'Timestamp', 'Camera Make', 'Camera Model', 'GPS Lat.', 'GPS Long.'])

# list of files in user-specified var `directory`
fileNames = []

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

# Attempt to open the directory specified by the user
try:
    fileNames = os.listdir(directory)
    # Print the specified directory and omit from table to save space
    print('Processing JPEG files in:\n   ' + os.path.abspath(directory))
    separator(promptLen)

    for eachFile in fileNames:
        path = os.path.abspath(directory)
        IMG = verifyAndProcessJPG(path, eachFile)
        if IMG:
            table.add_row(IMG.GenerateListRow())

    count = 0
    for each in table:
        count += 1

    if count > 0:
        printTable(table)
        print('NOTICE: Images without proper read-permissions will not have metadata')
    else:
        print("NOTICE: No JPEG-encoded images in directory.", end='\n\n')

# Print error and close end program
except (NotADirectoryError, FileNotFoundError) as e:
    print(e)
