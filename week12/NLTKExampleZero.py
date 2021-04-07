'''
Simple introduction to NLTK Usage
March 2021
Professor Hosmer
'''
# Standard Libraries

# 3rd Party Libraries

import nltk     # Import the Natural Language Toolkit
from nltk.corpus import PlaintextCorpusReader, stopwords   #Import the PlainTextCorpusReader Module
from nltk import word_tokenize, pos_tag, FreqDist, trigrams
from prettytable import PrettyTable
import re 

# Read all contents of the corpus
Corpus    = PlaintextCorpusReader('./CORPUS', '.*')
rawText   = Corpus.raw()
rawText   = re.sub("[^a-zA-Z' ]", ' ', rawText)   
  
# Extract tokens from the raw text
tokens = nltk.word_tokenize(rawText)
TextCorpus = nltk.Text(tokens)  

print("Tokens Extracted: ",len(tokens))
print("Compiling Vocabulary Frequencies")
print(TextCorpus.vocab())




