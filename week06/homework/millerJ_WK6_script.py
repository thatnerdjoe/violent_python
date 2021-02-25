from bs4 import BeautifulSoup as bs4
from prettytable import PrettyTable as ptables
from urllib.parse import urlparse
import os
import sys
import requests

SCRIPT_AUTHOR = 'Joseph Miller'
SCRIPT_NAME = 'Assignment 9 - Web Scraping'
SCRIPT_DATE = '2021-02-24'

'''
PROMPT:

    Using the Exp-14, Exp-15 and Exp-16 as a guide along with this weeks
    lecture you are to create a script that will extract the following
    information from a web-page.  You will be using the Python Standard
    Library requests and the 3rd Party Library BeautifulSoup4 along
    with other Python standard libraries as necessary.

    For the web-page, you will extract the following information

        page-title
        page-links URLs
        images found on the page

    You will submit

        1) Your completed script including comments.

        2) A document that contains the output from your
            script (title, links, and images extracted).
'''
###
# GLOBAL VARS
###


TARGET_URL = 'https://casl.website'
# Converted basename of URL (e.g.: google.com -> google_com)
CONV_NETLOC = urlparse(TARGET_URL).netloc.replace('.', '_')
# Directory name of new directory in PWD
OUTLOC = os.path.basename('./' + CONV_NETLOC)
# Output file (links.txt)
OUTFILE = os.path.join(OUTLOC, 'links.txt')

###
# FUNCTIONS
###

# Not implemented, but should allow user to enter URL as CLI arg
#
# def checkArgs(args):
#     '''
#     Checks for proper CLI arguments and sets them accordingly
#     '''
#     if (len(args) < 2):
#         print("\nNot enough arguments.\n"
#               "Expected: " + args[0] + " [URL]\n"
#               "Exiting...")
#         exit(1)
#     else:
#         TARGET_URL = args[1]
#         # Parse the URL provided and check if it has valid schema
#         check = urlparse(TARGET_URL)
#         # Assign other variables if schema found
#         if (check[0]):
#             NETLOC = urlparse(TARGET_URL).netloc.replace('.', '_')
#             OUTFILE = NETLOC + '.txt'
#             OUTLOC = os.path.basename('./' + NETLOC)
#         # Otherwise, prompt user and exit program
#         else:
#             print('Invalid URL "' + TARGET_URL + '": No schema supplied.\n'
#                   'Perhaps you meant http://' + TARGET_URL + ' ?')
#             exit(1)


def processImgs(soup):
    print("Extracting IMAGES from: ", TARGET_URL)
    print("Please wait...")

    images = soup.findAll('img')  # Find the image tags
    for eachImage in images:      # Process and display each image
        try:
            imgURL = eachImage['src']
            print("Processing Image:", imgURL, end="")
            if imgURL[0:4] != 'http':       # If URL path is relative
                imgURL = TARGET_URL+imgURL         # try prepending the base url

            # Get the image from the URL
            response = requests.get(imgURL)
            imageName = os.path.basename(imgURL)

            imgOutputPath = os.path.join(os.getcwd(), OUTLOC, imageName)

            with open(imgOutputPath, 'wb') as outFile:
                outFile.write(response.content)

            # Save the image
            print("  >> Saved Image:", imgOutputPath)
        except Exception as err:
            print(imgURL, err)
            continue


def processLinks(soup):
    print("Extracting LINKS from: ", TARGET_URL)
    print("Please wait...")

    temp_list = []

    links = soup.findAll('a', href=True)  # Find the anchor tags with links
    for eachLink in links:      # Process each link
        try:
            href = eachLink['href']
            if href[0:4] != 'http':               # If URL path is relative
                href = TARGET_URL+href         # try prepending the base url

            temp_list.append(href)  # append next URL href to list

        except Exception as err:
            print(href, err)
            continue
    return temp_list


def separator(l):
    '''
    Line break made from '=' characters
    '''
    for x in range(l):
        print('=', end='')
    print()


def printTable(table, file_name=None):
    '''
    Callable function to print the PrettyTable obj
    with various formatting args. Will print table to
    file if passed a file descriptor.
    '''
    table.align = 'l'
    if (file_name == None):
        print(table.get_string())
    else:
        file_desc = open(file_name, 'a')
        file_desc.write(table.get_string())
        file_desc.close()
        print(f'Wrote to file {file_desc.name}\n')


###
# CLASSES
###

# NONE


###
# MAIN SCRIPT
###
table = ptables(['Link Count', 'Link URL'])
site_title = ''
processed_links = []

print('\n' + SCRIPT_AUTHOR + '\n' + SCRIPT_NAME + '\n' + SCRIPT_DATE)
separator(45)

# Request URL
page = requests.get(TARGET_URL)

# Create BS4 Object
soup = bs4(page.text, 'html.parser')

# Create a new subdirectory named after the TARGET_URL
# Notify user if path exists
try:
    os.mkdir(OUTLOC)
except Exception as err:
    print("NOTICE: Directory " +
          os.path.join(os.getcwd(), OUTLOC) + " already exists")

# Parse and store data (title, links, images)
# Find first instance <title> tags and remove HTML components
site_title = soup.findAll('title')[0].get_text()
# Extract all links on the page and store in a list
processed_links = processLinks(soup)
print("Link extraction complete!")
separator(45)

# Extract images from TARGET_URL, saved in a subdirectory
# named after the base URL in the form: 'name_tld'
processImgs(soup)
print("Image extraction complete!")
separator(45)

# Add links to a PrettyTable for output to file
for count, eachLink in enumerate(processed_links):
    table.add_row([str(count+1), eachLink])

# Output to file
file_desc = open(OUTFILE, 'w')
file_desc.write('Site title: ' + site_title + '\n')
file_desc.close()

print('Dumping links...')
printTable(table, OUTFILE)
