'''
Week One Assignment - Simple String Searching
'''
# Prompt 1
SCRIPT_NAME = "Script: Simple String Searching"
SCRIPT_AUTHOR = "Author: Joseph Miller"
SCRIPT_NUMBER = "Assignment #1"
'''
Given excerpt from the hacker manifesto

Complete the script below to do the following:
1) Add your name, date, assignment number to the top of this script
2) Convert the string to all lower case
3) Count the number characters in the string
4) Count the number of words in the string
5) Sort the words in alphabetical order
6) Search the excerpt variable given below
   For the following and report how many occurances of each are found
   scandal
   arrested
   er
   good
   tomorrow
7) Submit
   NamingConvention: lastNameFirstInitial_Assignment_.ext
   for example:  hosmerC_WK1_script.py
                 hosmerC_WK1_screenshot.jpg
   A) Screenshot of the results in WingIDE
   B) Your Script
'''

excerpt = " Another one got caught today, it's all over the papers. Teenager\
            Arrested in Computer Crime Scandal, Hacker Arrested after Bank Tampering\
            Damn kids.  They're all alike"

''' Your work starts here '''

if __name__ == '__main__':

    # Print Basic Script Information

    print("Prompt #1)")
    print('\t   ' + SCRIPT_NAME)
    print('\t   ' + SCRIPT_AUTHOR)
    print('\t   ' + SCRIPT_NUMBER)

    punct = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
    searchList = ['scandal', 'arrested', 'er', 'good', 'tomorrow']

   # Practicing list comprehension and functional programming

    # remove excess whitespace from excerpt
    excerptLowercase = ' '.join(excerpt.split()).lower()

    # remove trailing punct within `excerpt`
    excerptNoPunct = ''.join(
        i if i not in punct else '' for i in excerptLowercase)

    # split `noPunct` into a list of words
    excerptListed = [i.lower() for i in excerptNoPunct.split(' ')]

    # sort `excerptList` alphabetically and save as a string
    excerptSorted = ' '.join(sorted(excerptListed))

    print('\nPrompt #2) ' + excerptLowercase)

    print('\nPrompt #3) There are ' + str(len(excerptLowercase)) +
          ' characters in the string.')

    # `excerptSorted` string is split into a list and then the number of words counted
    print('\nPrompt #4) There are ' + str(len(excerptSorted.split(" "))) +
          ' words in the string.')

    print('\nPrompt #5) ' + excerptSorted)

    print('\nPrompt #6) ' + '\t   '.join('"' + w + '"' + ' occurs: ' + str(excerptLowercase.count(w)) + ' times in string.\n'
                                         for w in searchList))

    # End of Script Main
