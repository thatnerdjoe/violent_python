'''
List Processing Mixed Types
Python Review
Sat February 20, 2021
Professor Hosmer
'''

# Create empty an dictionary, set and list
testDict = {}
testSet  = set()
testList = []

testDict['Criminal'] = 'John Gotti'
testDict['Terrorist'] = "Osama Bin Laden"
testDict['Serial Killers'] = ["Ted Bundy", "Jack the Ripper", "Jeffrey Dahmer"]
print("Dictionary\n", testDict)

testSet.add(1999)
testSet.add(2000)
testSet.add(2001)
testSet.add(2021)
print("Set\n",testSet)

print("\nSimple List Example")
testList.append("Steve Jobs")
testList.append("Bill Gates")
testList.append("Alan Turing")
print("List\n",testList)

testList.append(testDict)
print("List with added Dictionary\n", testList)

testList.append(testSet)
print("List with added Dictionary and Set\n", testList)

print("\nPrint by Type\n")
for eachEntry in testList:
    if isinstance(eachEntry, str):
        print("\tString")
        print("\t\t", eachEntry)
    if isinstance(eachEntry, dict):
        print("\tDictionary Contents")
        for key, value in eachEntry.items():
            print("\t\t",key, value)
    if isinstance(eachEntry, set):
        print("\tSet Contents")
        for value in eachEntry:
            print("\t\t",eachEntry)
            
print("\nScript Terminated")