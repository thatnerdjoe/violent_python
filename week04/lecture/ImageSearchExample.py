'''
Image Search 
Example
'''

# Python Standard Library
import os

# 3rd Party Modules
from PIL import Image
from prettytable import PrettyTable


# Files to Process
testFile = "test.jpg"
tbl = PrettyTable(['Image?','File', 'FileSize', 'Ext', 'Format', 'Width', 'Height', 'Type'])    

absPath = os.path.abspath(testFile)
ext = os.path.splitext(absPath)[1]
fileSize = '{:,}'.format(os.path.getsize(absPath))

try:
    # Try to open as an image
    with Image.open(absPath) as im:
        # if success, get the details
        imStatus = 'YES'
        imFormat = im.format
        imMode   = "?"        # hint im.mode
        imWidth  = "?"
        imHeight = "?"
        
        ''' Create a table row for each image, and record any extension mis-match alert '''
        tbl.add_row([imStatus, absPath, fileSize, ext, imFormat, imWidth, imHeight, imMode])
except:
    imStatus = 'NO'
    # else, not a valid image
    tbl.add_row([imStatus, absPath, fileSize, ext, 'NA', 'NA', 'NA', 'NA'])            
tbl.align = 'l'
print(tbl.get_string())

