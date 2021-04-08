#
# NLTK QUERY Example
# Professor Hosmer
# August 2020

"""
Modified by: Joseph Miller
Purpose of changes: CYBV 473
Date: 04-07-2021

refer to requirements.txt for required packages to install
"""


import os       # Standard Library OS functions
import sys
import logging  # Standard Library Logging functions
import nltk     # Import the Natural Language Toolkit
# Import the PlainTextCorpusReader Module
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from time import sleep
from collections import Counter
from prettytable import PrettyTable

stopSet = set(stopwords.words('english'))


class classNLTKQuery:
    ''' NLTK Query Class '''

    def textCorpusInit(self, thePath):

        # Validate the path is a directory
        if not os.path.isdir(thePath):
            return "Path is not a Directory"

        # Validate the path is readable
        if not os.access(thePath, os.R_OK):
            return "Directory is not Readable"

        # Attempt to Create a corpus with all .txt files found in the directory
        try:

            self.Corpus = PlaintextCorpusReader(thePath, '.*')
            print("Processing Files : ")
            print(self.Corpus.fileids())
            print("Please wait ...")
            self.rawText = self.Corpus.raw()
            self.tokens = nltk.word_tokenize(self.rawText)
            self.filtered_tokens = [w for w in self.tokens if not w in stopSet]
            self.TextCorpus = nltk.Text(self.filtered_tokens)
            self.CollCorpus = nltk.BigramCollocationFinder.from_words(
                self.tokens)
        except:
            return "Corpus Creation Failed"

        self.ActiveTextCorpus = True

        return "Success"

    def printCorpusLength(self):
        print(f"\n\nCorpus Text Length:  {len(self.rawText)}")

    def printTokensFound(self):
        print(f"\n\nTokens Found:  {len(self.tokens)}")

    def printVocabSize(self):
        print("\n\nCalculating Vocabulary Size...")
        print(f"\nVocabulary Size:   {len(self.TextCorpus.vocab())}")

    def printCollocation(self):
        """
        Would have simply used
            self.TokenCorpus.collocation()
        method, but the bigrams seemed to be random. Used the API docs
        to create a BigramCollocationFinder obj for this. Turns out the
        outputs are the same, but with the added field denoting the score
        """
        print("\n\nCompiling Top 100 Collocations ...\n")
        def filteredStops(w): return len(w) < 3 or w in stopSet
        self.CollCorpus.apply_word_filter(filteredStops)
        collocations = self.CollCorpus.score_ngrams(
            BigramAssocMeasures.likelihood_ratio)
        for idx, each in enumerate(collocations):
            if idx == 100:
                break
            print(each)

    def searchWordOccurrence(self):
        myWord = input("\n\nEnter Search Word : ")
        if myWord:
            print(f"Searching for \"{myWord}\"\n")
            print(f"{myWord} occurs {self.TextCorpus.count(myWord.upper())} times")

    def generateConcordance(self):
        myWord = input("\n\nEnter word to Concord : ")
        if myWord:
            print("Compiling First 100 Concordance Entries ...\n")
            sleep(1)
            self.TextCorpus.concordance(myWord, lines=100)

    def generateSimiliarities(self):
        myWord = input("\n\nEnter seed word : ")
        if myWord:
            print("Compiling First 200 Similiarity Entries ...\n")
            self.TextCorpus.similar(myWord, num=200)

    def printWordIndex(self):
        myWord = input("\n\nFind first occurrence of what Word? : ")
        if myWord:
            print(f"Searching for first occurrence of \"{myWord}\"\n")
            print(
                f"\"{myWord}\" first found at index {self.TextCorpus.index(myWord.upper())}")

    def printVocabulary(self):
        print("\n\nCompiling Vocabulary Frequencies")

        tbl = PrettyTable(["Vocabulary", "Occurs"])
        vocab = self.TextCorpus.vocab()
        for samples in vocab:
            tbl.add_row([samples, vocab[samples]])

        print(tbl)

def printMenu():

    # Function to print the NLTK Query Option Menu

    print("==========NLTK Query Options =========")
    print("[1]    Print Length of Corpus")
    print("[2]    Print Number of Token Found")
    print("[3]    Print Vocabulary Size")
    print("[4]    Print Collocations")
    print("[5]    Search for Word Occurrence")
    print("[6]    Generate Concordance")
    print("[7]    Generate Similarities")
    print("[8]    Print Word Index")
    print("[9]    Print Vocabulary")
    print()
    print("[0]    Exit NLTK Experimentation")

    print()

 # Function to obtain user input


def getUserSelection():
    printMenu()


    while True:
        try:
            sel = input('Enter Selection (0-9) >> ')
            menuSelection = int(sel)
        except ValueError:
            print('Invalid input. Enter a value between 0-9.')
            continue

        if not menuSelection in range(0, 10):
            print('Invalid input. Enter a value between 0-9.')
            continue

        return menuSelection


if __name__ == '__main__':

    print("Welcome to the NLTK Query Experimentation")
    print("Please wait loading NLTK ... \n")

    print("Input full path name where intended corpus file or files are stored")
    print("Format for Windows e.g. ./CORPUS \n")

    userSpecifiedPath = input("Path: ")

    # Attempt to create a text Corpus
    oNLTK = classNLTKQuery()
    result = oNLTK.textCorpusInit(userSpecifiedPath)

    if result == "Success":

        menuSelection = -1

        while menuSelection != 0:

            if menuSelection != -1:
                print()
                s = input('Press Enter to continue...')

            menuSelection = getUserSelection()

            try:
                if menuSelection == 1:
                    oNLTK.printCorpusLength()

                elif menuSelection == 2:
                    oNLTK.printTokensFound()

                elif menuSelection == 3:
                    oNLTK.printVocabSize()

                elif menuSelection == 4:
                    oNLTK.printCollocation()

                elif menuSelection == 5:
                    oNLTK.searchWordOccurrence()

                elif menuSelection == 6:
                    oNLTK.generateConcordance()

                elif menuSelection == 7:
                    oNLTK.generateSimiliarities()

                elif menuSelection == 8:
                    oNLTK.printWordIndex()

                elif menuSelection == 9:
                    oNLTK.printVocabulary()

                elif menuSelection == 0:
                    print("Goodbye")
                    print()

                elif menuSelection == -1:
                    continue

                else:
                    print("unexpected error condition")
                    menuSelection = 0

            except Exception as e:
                print(e)

            sleep(1)

    else:
        print("Closing NLTK Query Experimentation")
