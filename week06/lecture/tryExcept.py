'''
try/except usage
Python Review
Sat February 20, 2021
Professor Hosmer
'''
from binascii import hexlify

print("\nExample One")

while True:
    
    try:
        numerator = input("\nPlease Enter the Numerator:   ")
        if numerator.lower() == 'q':
            break
        denomenator = input("Please Enter the Denominator: ")
        result = int(numerator) / int(denomenator)
        print("Numerator / Denomenator= ", result)
    except Exception as err:
        print("\nException: ", str(err))
    
print("\nExample Two")        
while True:
    
    try:
        filePath = input("\nPlease Enter a Filename: ")
        if filePath.lower() == 'q':
            break
        with open(filePath, 'rb') as readTheFile:
            fileContents = readTheFile.read()
            print(filePath, " :", hexlify(fileContents[:20]))
    except Exception as err:
        print("\nException: ", str(err))
        print("oh no")
print("\nUser terminated the script")