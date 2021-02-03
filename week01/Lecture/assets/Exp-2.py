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
from __future__ import print_function
#
# Experiment Two - Built In Types


#
# Boolean Types
#
print("\nPython Built-in Types\n")

print("Python Boolean Types\n")

status = True
print(type(status))

if status:
    print("Status is True")
else:
    print("Status is False")

status = False
print(type(status))

if status:
    print("Status is True")
else:
    print("Status is False")
    
#
# Truth Testing non Boolean Types
#

print("\nPython Truth Testing non Boolean Types\n")

myString = ''
print(type(myString))
if myString:
    print(myString)
else:
    print("myString is Empty")
    
myString = 'Hello World'
print(type(myString))
if myString:
    print(myString)
else:
    print("myString is Empty")  

myList = []
print(type(myList))

if myList:
    print(myList)
else:
    print("myList is Empty")  

myList = ["Hello", "World", 42, 76.8, 0x22, [2,4,6]]
print(type(myList))

if myList:
    print(myList)
else:
    print("myList is Empty") 

#    
# Boolean Operations
#

print("\nPython Boolean Operations\n")

A = True
B = False

# A or B

if A or B:
    print("True")
else:
    print("False")
    
# A and B

if A and B:
    print("True")
else:
    print("False")
    
#
# Comparison Operations
#

print("\nPython Comparison Operations\n")

A = 47
B = 14

if A == B:
    print("A = B")
else:
    print("A Not Equal to B")
    
if A < B:
    print("A is less than B")
else:
    print("A is not less than B")
    
if A > B:
    print("A is greater than B")
else:
    print("A is not greater than B")
    
if A <= B:
    print("A is less or equal to B")
else:
    print("A is not less nor equal to B")
    
if A >= B:
    print("A is greater than or equal to B")
else:
    print("A is not greater nor equal to B")

if A != B:
    print("A is not equal to B")
else:
    print("A is equal to B")
    
print("\nPython Numeric Types\n")

myInt = 47
myFloat = 47.1

print(type(myInt))
print(type(myFloat))

#
#Python Numeric Operations
#

print("\nPython Numeric Operations\n")

x = 7
y = 4
print("x:    ",x)
print("y:    ",y)
print("x+y:  ",x+y)
print("x*y:  ",x*y)
print("x/y:  ",x/y)
print("x//y: ",x//y)
print("x%y:  ",x%y)
print("-x:   ",-x)
print("+x:   ",+x)
print("x**y: ",x**y)

#
# Python Bitwise Operations
#

print("\nPython Boolean Operations\n")

a = 0b1010111
b = 0b0101101
print(a)
print(b)
print(hex(a))
print(hex(b))

print('a      {:08b}'.format(a))
print('b      {:08b}'.format(b))
print('a | b  {:08b}'.format(a | b))
print('a & b  {:08b}'.format(a & b))
print('a ^ b  {:08b}'.format(a ^ b))
print('a << 2 {:010b}'.format(a << 2))
print('a >> 2 {:08b}'.format(a >> 2))

# 
# Binary and Hex Rendering 
# Using the format method
#

print("\nPython Boolean Binary and Hex Rendering\n")

value = 254

print('Dec', value)
print('Hex {:02x}'.format(value).upper())
print('Bin {:08b}'.format(value).upper())


