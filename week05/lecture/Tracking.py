'''
quick dictionary example
counting occurrances
Professor Hosmer
Sept 2020
'''
import os

with open('dialog.txt') as target:
    
    fileContents = target.read()
    
    stringList = fileContents.split()
    
stringDictionary = {}

for eachString in stringList:
    
    lowerCaseString = eachString.lower()
    
    try:
        occurrances = stringDictionary[lowerCaseString]
        occurrances += 1
        stringDictionary[lowerCaseString] = occurrances
    except:
        stringDictionary[lowerCaseString] = 1

firstFiveList = list(stringDictionary.items())[0:5]
lastFiveList  = list(stringDictionary.items())[-5:]

print("FIRST FIVE:", firstFiveList)
print("LAST FIVE: ", lastFiveList)

allStringsList = list(stringDictionary.items())

allStringsList.sort(key = lambda x: x[1], reverse=True)
print(allStringsList[:10])
print(allStringsList[-10:])

print("\nFirst 100")
for eachEntry in allStringsList[:100]:
    print(eachEntry)
    
print("\nLast 100")
for eachEntry in allStringsList[-100:]:
    print(eachEntry)
    
print("\nend script")



    


    
    