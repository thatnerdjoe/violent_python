'''
Pretty Table Example
prettytable wiki documentation: 
https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki
'''

# Import Python Standard Libraries
import os
import sys
import time

# Import 3rd Party Library
from prettytable import PrettyTable

# Create Prettytable with Heading
myTable = PrettyTable(['FileName', 'Type', 'FileSize', 'LastModified', 'epoch'])

# set a directory to scan
root = 'c:/'

try:
    # Get a list of files    
    fileList = os.listdir(root)
    
    # Loop through each file
    for eachFile in fileList:
        # Get the full path
        path = os.path.join(root, eachFile)
        
        if os.path.isfile(path):
            fileType = "File"
        elif os.path.isdir(path):
            fileType = "Dir"
        elif os.path.islink(path):
            fileType = "Link"
        else:
            fileType = "Unknown"
            
        # obtain the stats 
        fileStats = os.stat(path)
        
        # Extract required properties
        fileSize = fileStats.st_size
        lastModEpoch = fileStats.st_mtime
        lastMod = time.ctime(lastModEpoch)
        
        # add a row to the table for each file
        myTable.add_row([path, fileType, fileSize, lastMod, lastModEpoch])
        
except Exception as err:
    sys.exit("Err: "+str(err))
     
myTable.align='l'
myTable.hrules=1
output = myTable.get_string()
#output = myTable.get_string(sortby='Type')
#output = myTable.get_string(sortby='epoch', reversesort=True)
#output = myTable.get_string(sortby='FileSize', reversesort=True)
print(output)