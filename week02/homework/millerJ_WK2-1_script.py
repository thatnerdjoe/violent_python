from __future__ import print_function
import os
'''
Week Two Assignment 1 - File Processing

Author:     Joseph Miller
Date:       Jan 21, 2021
Assignment: #2-1
'''
SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_DATE = 'Jan 27, 2021'
SCRIPT_NAME = 'Assignment #2-1: Log Parser'
'''
Complete the script below to do the following:
1) Add your name, date, assignment number to the top of this script
2) Open the file redhat.txt 
   a) Iterate through each line of the file
   b) Split eachline into individual fields (hint str.split() method)
   c) Examine each field of the resulting field list
   d) If the word "worm" appears in the field then add the worm name to the set of worms
   e) Once you have processed all the lines in the file
      sort the set 
      iterate through the set of worm names
      print each unqiue worm name 
3) Submit
   NamingConvention: lastNameFirstInitial_Assignment_.ext
   for example:  hosmerC_WK2-1_script.py
                 hosmerC_WK2-2_screenshot.jpg
   A) Screenshot of the results in WingIDE
   B) Your Script
'''

print(SCRIPT_AUTHOR)
print(SCRIPT_DATE)
print(SCRIPT_NAME)
print()

uniqueWorms = set()

with open("redhat.txt", 'r') as logFile:
    for eachLine in logFile:
        lineContents = eachLine.split()
        for eachItm in lineContents:
            if 'worm' in eachItm.lower():
                uniqueWorms.add(eachItm)

sortedUniqueWorms = sorted(uniqueWorms)

for eachItm in sortedUniqueWorms:
    print(eachItm)
