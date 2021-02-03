'''
Copyright (c) 2019 Python Forensics, Inc.
                   
Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

'''

# Experimenting with Python Strings

print("\nPython String\n")

s = "the quick brown fox jumps over the lazy dog"

print("characters: ",len(s))
print("capitalize:", s.capitalize())
print("upper case:", s.upper())
print("lower case:", s.lower())
print("Count o:   ", s.count('o'))

print("s[0,4] : ", s[0:4])
print("s[8:]  : ", s[8:])
print("s[9:12]: ", s[9:12])

if 'brown' in s:
    print("Found brown")
else:
    print("brown Not Found")

if 'Brown' in s:
    print("Found Brown")
else:
    print("Brown Not Found")
    
if 'BROWN' in s.upper():
    print("Found BROWN")
else:
    print("BROWN Not Found")
    
stringSplit = s.split()
print("Strings: ",len(stringSplit))

print("s.split returns :", type(stringSplit))
print("s.split: ", stringSplit)
stringSplit.sort()
print("s.split Sorted: ", stringSplit)

print("The Ordinal Value of the first character: ", ord(s[0]))

if s.endswith('dog'):
    print("String ends with dog")
else:
    print("Sting does not end with dog")

if s.endswith('cat'):
    print("String ends with cat")
else:
    print("String does not end with cat")
    
    
