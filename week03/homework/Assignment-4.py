from __future__ import print_function

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

import os






        
        
