import json
import hashlib
import os
from virus_total_apis import PublicApi as VirusTotalPublicApi


SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'VirusTotal Sample API Client'
SCRIPT_DATE = '2021-04-22'

"""
Assignment #19

    For this week's assignment, you will be creating a simple VirusTotal Client.

        1. Your client will prompt the user for a filename

        2. You will hash the specified file

        3. Use the VirusTotal API to check to see if the file hash exists in Virus Total

        NOTE: it is NOT necessary to select a known file that contains a virus or malware

    You will submit your script and a screenshot of successful execution.

    Professor Hosmer
"""

###
#  FUNCTIONS
###


def separator(leng=40):
    print('='*leng)

###
# CLASSES - NONE
###


###
# MAIN
###
if __name__ == '__main__':

    # ENV VARS
    ENV_API_TOKEN = 'VTAPI'
    API_KEY = os.getenv(ENV_API_TOKEN)

    # Program vars
    chunkSize = 256
    sha256sum = ''

    # Prompt for user
    prompt = 'Please, enter the path of a binary file: '

    # Print header
    separator()
    print('\n' + SCRIPT_AUTHOR + '\n' + SCRIPT_NAME +
          '\n' + SCRIPT_DATE, end='\n\n')
    separator()

    # Prompt for user input
    filePath = input(prompt)
    separator()

    try:
        print(f'Generating SHA256 for file "{filePath}"...')
        with open(filePath, 'rb') as binaryFile:
            hashObj = hashlib.sha256()

            while True:
                chunk = binaryFile.read(chunkSize)

                if len(chunk) > 0:
                    hashObj.update(chunk)

                else:
                    sha256sum = hashlib.md5().hexdigest()
                    break

    except:
        print('\nERROR: Could not open file!\nEnsure proper read permissions exist.\n')

    vt = VirusTotalPublicApi(API_KEY)

    response = vt.get_file_report(sha256sum)
    print(json.dumps(response, sort_keys=False, indent=4))
