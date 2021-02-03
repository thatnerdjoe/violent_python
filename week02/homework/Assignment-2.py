from __future__ import print_function
import os

'''
Week Two Assignment 1 - File Processing
'''
SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_DATE = 'Jan 27, 2021'
SCRIPT_NAME = 'Assignment #2: Log Parser'
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


uniqueWorms = set()

with open("redhat.txt", 'r') as logFile:
    for eachLine in logFile:
        ''' your code starts here '''
