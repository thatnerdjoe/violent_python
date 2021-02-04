'''
EXIF Data Acquistion Example
January 2019
Version 1.1
'''

'''
Using this script provide as a baseline.
Expand the script as follows:

1) Allow the user to enter a path to a directory containing jpeg files.
2) Using that path, process only the .jpg files contained in that folder  (use the testimages.zip set of images)
3) Extract, EXIF data from each of the images and create a pretty table output
   Note, your script can extract other EXIF data that you find interesting
4) Finally, you will Plot the geolocation of each image on a map.

NOTE: There are several ways to do this, however, the easiest method would be to use the MapMaker App, at https;//mapmakerapp.com/
      you can either manually enter the lat/lon values your script generates or you can place your results in a CSV file and upload
      the data to the map.

'''
# Usage Example:
# python Assignment 6
#
# Requirement: Python 3.x
#
# Requirement: 3rd Party Library that is utilized is: PILLOW
#                   pip install PILLOW  from the command line
#                   this is already installed in the Virtual Desktop


''' LIBRARY IMPORT SECTION '''

import os                       # Python Standard Library : Operating System Methods
import sys                      # Python Standard Library : System Methods
from datetime import datetime   # Python Standard Libary datetime method from Standard Library

# import the Python Image Library 
# along with TAGS and GPS related TAGS
# Note you must install the PILLOW Module
# pip install PILLOW

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


# import the prettytable library
from prettytable import PrettyTable

def ExtractGPSDictionary(fileName):
    ''' Function to Extract GPS Dictionary '''
    try:
        pilImage = Image.open(fileName)
        exifData = pilImage._getexif()

    except Exception:
        # If exception occurs from PIL processing
        # Report the 
        return None, None

    # Interate through the exifData
    # Searching for GPS Tags

    imageTimeStamp = "NA"
    cameraModel = "NA"
    cameraMake = "NA"
    gpsData = False

    gpsDictionary = {}

    if exifData:

        for tag, theValue in exifData.items():

            # obtain the tag
            tagValue = TAGS.get(tag, tag)
            print(tagValue)
            # Collect basic image data if available

            if tagValue == 'DateTimeOriginal':
                imageTimeStamp = exifData.get(tag).strip()

            if tagValue == "Make":
                cameraMake = exifData.get(tag).strip()

            if tagValue == 'Model':
                cameraModel = exifData.get(tag).strip()

            # check the tag for GPS
            if tagValue == "GPSInfo":

                gpsData = True;

                # Found it !
                # Now create a Dictionary to hold the GPS Data

                # Loop through the GPS Information
                for curTag in theValue:
                    gpsTag = GPSTAGS.get(curTag, curTag)
                    gpsDictionary[gpsTag] = theValue[curTag]

        basicExifData = [imageTimeStamp, cameraMake, cameraModel]    

        return gpsDictionary, basicExifData

    else:
        return None, None

# End ExtractGPSDictionary ============================


def ExtractLatLon(gps):
    ''' Function to Extract Lattitude and Longitude Values '''

    # to perform the calcuation we need at least
    # lat, lon, latRef and lonRef
    
    try:
        latitude     = gps["GPSLatitude"]
        latitudeRef  = gps["GPSLatitudeRef"]
        longitude    = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]

        lat, lon = ConvertToDegreesV1(latitude, latitudeRef, longitude, longitudeRef)

        gpsCoor = {"Lat": lat, "LatRef":latitudeRef, "Lon": lon, "LonRef": longitudeRef}

        return gpsCoor

    except Exception as err:
        return None

# End Extract Lat Lon ==============================================


def ConvertToDegreesV1(lat, latRef, lon, lonRef):
    
    degrees = lat[0]
    minutes = lat[1]
    seconds = lat[2]
    latDecimal = float ( (degrees +(minutes/60) + (seconds)/(60*60) ) )
    if latRef == 'S':
        latDecimal = latDecimal*-1.0
        
    degrees = lon[0]
    minutes = lon[1]
    seconds = lon[2]
    lonDecimal = float ( (degrees +(minutes/60) + (seconds)/(60*60) ) )
    
    if latRef == 'W':
        lonDecimal = lonDecimal*-1.0
    
    return(latDecimal, lonDecimal)


''' MAIN PROGRAM ENTRY SECTION '''

if __name__ == "__main__":
    '''
    pyExif Main Entry Point
    '''
    print("\nExtract EXIF Data from JPEG Files")

    print("Script Started", str(datetime.now()))
    print()

    ''' PROCESS EACH JPEG FILE SECTION '''

    latLonList = []
    targetFile = "biking.jpg"                 # file must be located in the same folder
    if os.path.isfile(targetFile):
        gpsDictionary, exifList = ExtractGPSDictionary(targetFile)
            
        if exifList:
            TS = exifList[0]
            MAKE = exifList[1]
            MODEL = exifList[2]
        else:
            TS = 'NA'
            MAKE = 'NA'
            MODEL = 'NA'

        print("Photo Details")
        print("-------------")
        print("TimeStamp:    ", TS)
        print("Camera Make:  ", MAKE)
        print("Camera Model: ", MODEL)
        
        if (gpsDictionary != None):

            # Obtain the Lat Lon values from the gpsDictionary
            # Converted to degrees
            # The return value is a dictionary key value pairs

            dCoor = ExtractLatLon(gpsDictionary)

            print("\nGeo-Location Data")
            print("-----------------")

            if dCoor:
                lat = dCoor.get("Lat")
                latRef = dCoor.get("LatRef")
                lon = dCoor.get("Lon")
                lonRef = dCoor.get("LonRef")
                
                if ( lat and lon and latRef and lonRef):
                    print("Lattitude: ", '{:4.4f}'.format(lat))
                    print("Longitude: ", '{:4.4f}'.format(lon))
                else:
                    print("WARNING No GPS EXIF Data")
            else:
                print("WARNING No GPS EXIF Data")                    
        else:
            print("WARNING", " not a valid file", targetFile)

    # Create Result Table Display using PrettyTable
    ''' GENERATE RESULTS TABLE SECTION'''

    ''' Result Table Heading'''
    resultTable = PrettyTable(['File-Name', 'Lat','Lon', 'TimeStamp', 'Make', 'Model'])
    ''' Your work starts here '''
    
    print()