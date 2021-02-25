'''
User Directory Entry Example
Python Review
Sat February 20, 2021
Professor Hosmer
'''
import os           #Python Standard OS Libary

while True:
    print("\nUser Directory Entry Test")
    userDir = input("Please enter a valid directory path: ")
    if userDir.lower() == 'q':
        break
    if os.path.isdir(userDir):
        absPath = os.path.abspath(userDir)
        if os.access(absPath, os.R_OK):
            print("Directory: ", absPath, " is valid and readable")
            entryList = os.listdir(absPath)
            for eachEntry in entryList:
                print(eachEntry)
        else:
            print("Directory: ", abspath, " is valid but we do not have read access")
    else:
        print("Directory: ", userDir, " **** Invalid Directory")

print("\nUser terminated the script")