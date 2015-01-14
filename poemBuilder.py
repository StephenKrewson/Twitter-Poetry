### SECTION 1: PREPARATION ###
##############################
import re, sys, nltk, twitter, string, HTMLParser, pyttsx
from nltk.corpus import cmudict
from random import choice, randint
from nltk.tokenize import *
from nltk import FreqDist

# (1.1) Authenticate to Twitter using OAuth
api = twitter.Api(consumer_key='effBwIQZJUWIJvOqpw5y5A',
                  consumer_secret='AsNNfAsaVtK6PrpDne1YqFqQIreG1r2HF2AW52cU64',
                  access_token_key='403021421-XixLOL3CimN6ZZQ567jJLV2xCJhhW0mj1axcJZyu',
                  access_token_secret='8PDjjA8tOnaKmMZZ0JUJch9TLdtXTIzE6T0sMpGZw')

# (1.2) Store NLTK libraries (runtime atrocious if these are in the functions)
books = nltk.corpus.gutenberg.fileids()
lexicon = nltk.corpus.cmudict.dict()

### SECTION 2: FUNCTIONS ###
############################
def stripWord(word):
    """Returns tuple of stripped word, lexical stress count"""
    stress = 0
    word = HTMLParser.HTMLParser().unescape(word)
    stripped = word.lower().translate(string.maketrans('',''), string.punctuation)
    # Regex filters out hashtags, URLs
    if not re.match(r'\"*[@#]|http|RT', word):
        if stripped in lexicon:
            for j in ''.join(lexicon[stripped][0]):
                if j in ('1', '2'): # CMU dict has stress values of 1 or 2
                    stress += 1
            return word.encode('utf-8'), stress
        else: # Unknown words approximated as 1 total stress
            return word.encode('utf-8'), 1                        

def buildBackground(num):
    """Generates a random chunk of Project Gutenberg text"""
    # Grab a whole book with random 'choice' method
    background = nltk.corpus.gutenberg.raw(choice(books)).replace('\n', ' ').encode('utf-8')
    # Random start point with enough room for selection of 'num' length
    start = randint(0, len(background) - int(num))
    return background[start:start + int(num)]

def buildPoem(string, num, span=80):
    """Returns an array of lines determined by number of stresses"""
    poem, raw_poem, line, stress = [], [], '', 0
    fill = buildBackground(10000)
    index = 0
    search = api.GetSearch(string)
    # Grab body of tweets with 'text' method; turn everything into Unicode
    corpus = [s.text.encode('utf-8') for s in search]
    # Join into single array; strip endmarks, whitespace
    for word in ' '.join(corpus).split():
        try:
            stripped = stripWord(word)
            stress += stripped[1]
            if stress < 7:
                line += stripped[0] + ' '
            else:
                start = randint(0, span - len(line))
                raw_poem.append(line.encode('utf-8'))
                poem.append((fill[index:start + index], line.encode('utf-8'), fill[start + index:index + span - len(line)]))
                index += span - len(line)
                stress = 1
                line = stripped[0] + ' ' 
        except: ValueError # stripWord will not return non-words
    return poem, raw_poem

def storeResults(poem):
    """Append output of buildPoem to a master data file"""
    with open('data.txt', 'ab') as f:
        f.write(' '.join(poem))

def superFunction(string, num):
    """Puts everything together!"""
    poem = buildPoem(string, num)
    #storeResults(poem[1])
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-75)
    index = 0
    for i in poem[1]:
        index += 1
        print i
	#engine.say(i)
	#engine.runAndWait()
        if index % 4 == 0:
            print
    #' |||| '.join(i)
### SECTION 3: MAIN CODE ###
############################
superFunction(sys.argv[1], sys.argv[2])

