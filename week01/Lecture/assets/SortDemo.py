'''
Name: Chet Hosmer
Version: 1.0
Date: January 21, 2020
Script: Demonstration
'''

testString = "This is a test string with words 123456 98.6 $%#@@!"
print("\nString Contents and Type")
print(testString)
print(type(testString))
      
print("\nExtract Words from the string")
wordList = testString.split()

print("\nList Contents and Type")
print(wordList)
print(type(wordList))

print("\nSort the List in place")
wordList.sort()
print("\nsorted wordList contents")
print(wordList)

