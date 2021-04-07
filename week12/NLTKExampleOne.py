'''
Simple introduction to NLTK Usage
March 2021
Professor Hosmer
'''
# Standard Libraries

from collections import Counter

# 3rd Party Libraries

import nltk     # Import the Natural Language Toolkit
from nltk.corpus import PlaintextCorpusReader, stopwords   #Import the PlainTextCorpusReader Module
from nltk import word_tokenize, pos_tag, FreqDist, trigrams
from prettytable import PrettyTable
import re 

# PARTS of SPEECH Lookup
POSTAGS = {
        'CC':   'conjunction',
        'CD':   'CardinalNumber',
        'DT':   'Determiner',
        'EX':   'ExistentialThere',
        'FW':   'ForeignWord',
        'IN':   'Preposition',
        'JJ':   'Adjective',
        'JJR':  'AdjectiveComparative',
        'JJS':  'AdjectiveSuperlative',
        'LS':   'ListItem',
        'MD':   'Modal',
        'NN':   'Noun',
        'NNS':  'NounPlural',
        'NNP':  'ProperNounSingular',
        'NNPS': 'ProperNounPlural',
        'PDT':  'Predeterminer',
        'POS':  'PossessiveEnding',
        'PRP':  'PersonalPronoun',
        'PRP$': 'PossessivePronoun',
        'RB':   'Adverb',
        'RBR':  'AdverbComparative',
        'RBS':  'AdverbSuperlative',
        'RP':   'Particle',
        'SYM':  'Symbol',
        'TO':   'to',
        'UH':   'Interjection',
        'VB':   'Verb',
        'VBD':  'VerbPastTense',
        'VBG':  'VerbPresentParticiple',
        'VBN':  'VerbPastParticiple',
        'VBP':  'VerbNon3rdPersonSingularPresent',
        'VBZ':  'Verb3rdPersonSingularPresent',
        'WDT':  'WhDeterminer',
        'WP':   'WhPronoun',
        'WP$':  'PossessiveWhPronoun',
        'WRB':  'WhAdverb'
        }

# Read all contents of the corpus
stopWords = set(stopwords.words('english')) 
Corpus    = PlaintextCorpusReader('./CORPUS', '.*')
rawText   = Corpus.raw()
rawText   = re.sub("[^a-zA-Z' ]", ' ', rawText)   
  
# Extract tokens from the raw text
tokens = nltk.word_tokenize(rawText)
filteredTokens = [w for w in tokens if not w in stopWords] 
TextCorpus = nltk.Text(filteredTokens)  

print ("Compiling Vocabulary Frequencies")
print(TextCorpus.vocab())

# Take sampling of the parts of speech found
posTagged = pos_tag(filteredTokens[0:1000])

# Count the occurrences of each Part of Speech in the sample
posCounts = Counter(tag for word, tag in posTagged)

tbl = PrettyTable(['Count', 'POS', 'POS-TRANSLATED'])
for key, value in posCounts.items():
    try:
        translation = POSTAGS[key]
    except:
        continue
    tbl.add_row([value, key, translation])

tbl.align = 'l'
print(tbl.get_string(sortby='Count', reversesort=True))


