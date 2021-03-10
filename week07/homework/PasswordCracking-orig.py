'''
Rainbow Table Generator
and Password Cracker
Professor Hosmer

Assignment # 9

A password hash value has been intercepted during an investigation.
The hash value is of type md5 and is associated with a password
that is used by the suspect.

Your job is to brute force the password by generating all 
possible password combinations until you identify a matching
password.

A couple of additional details have been discovered.

1) A salt value is prepending to the password when hashing occurs
   and that have value is   &654P
   
2) The suspect is known to use 7 or 8 character passwords

3) The suspect is has a dog named boo

4) His favorite number is 11

5) and his hometown is rome

GIVEN: KNOWN HASH VAUE:  'e182221f74dbce5af2d6b3535cadb39e'
       PASSWORD LEN:  7 OR 8 characters
       SALT: &654P
       Dog: boo
       Favorite Number: 11
       HomeTown: rome

As a result you will provide a screenshot of your results

'''

# import standard libraries

import hashlib              # Hashing the results
import time                 # Timing the operation
import itertools            # Creating controled combinations

#
# Create a list of lower case, upper case, numbers
# and special characters to include in the password table
#

bruteForceCharacters = ['b', 'o', 'r', 'm', 'e', '1']

# Define a hypothetical SALT value
SALT = "&654P"
KNOWN_HASH = 'e182221f74dbce5af2d6b3535cadb39e'

# Define the allowable range of password length
PW_LOW = 7
PW_HIGH = 8

# Mark the start time
startTime = time.time()

# Create an empty list to hold the final passwords
pwList = []

# create a loop to include all passwords
# within the allowable range

print("Generating Passwords ... Please Wait")
pwCnt = 0
for r in range(PW_LOW, PW_HIGH+1):

    # Apply the standard library interator
    for s in itertools.product(bruteForceCharacters, repeat=r):
        # append each generated password to the
        # final list
        pwList.append(''.join(s))
        pwCnt += 1

# For each password in the list generate
# a hash value by concatenating
# the salt + password
# then report the resulting password

print("Possible Passwords Generated: ", pwCnt)
print("Searching for matching HASH: ", KNOWN_HASH)


try:
    passwordFound = False
    for pw in pwList:
        # Perform hashing of the password
        md5Hash = hashlib.md5()
        pwStr = (SALT+pw)
        pwStr = pwStr.encode('ascii')
        md5Hash.update(pwStr)
        md5Digest = md5Hash.hexdigest()
        if md5Digest == KNOWN_HASH:
            print("\nSUSPECT PASSWORD = ", pw, '\n')
            passwordFound = True
            break

    if not passwordFound:
        print("\nPASSWORD NOT FOUND\n")

except Exception as err:
    print('File Processing Error', err)

print("\nSCRIPT END")
