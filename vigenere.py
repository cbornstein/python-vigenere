'''
Clare Bornstein

vigenere.py

This program recovers the key of a message encrypted using the Vigerene Cipher.
The key length is recovered using the Kasiski analysis method from Invent with
Python. The key is recovered using a Chi-Square to perform frequency analysis
on the message as compared to a frequency table of letters in the English
language, and the found key length.


Frequency of Letters in English Language from Wikipedia:
https://en.wikipedia.org/wiki/Letter_frequency

Kasiski Analysis code is modified from Invent With Python:
https://inventwithpython.com/vigenereHacker.py
'''
import string

MAX_KEY_LENGTH = 50

vals = {'A': 0, 'B': 1, 'C': 2, 'D': 3,
        'E': 4, 'F': 5, 'G': 6, 'H': 7,
        'I': 8, 'J': 9, 'K': 10, 'L': 11,
        'M': 12, 'N': 13, 'O': 14, 'P': 15,
        'Q': 16, 'R': 17, 'S': 18, 'T': 19,
        'U': 20, 'V': 21, 'W': 22, 'X': 23,
        'Y': 24, 'Z': 25}
nums = { 0: 'A', 1: 'B', 2: 'C', 3: 'D',
         4: 'E', 5: 'F', 6: 'G', 7: 'H',
         8: 'I', 9: 'J', 10: 'K', 11: 'L',
         12: 'M', 13: 'N', 14: 'O', 15: 'P',
         16: 'Q', 17: 'R', 18: 'S', 19: 'T',
         20: 'U', 21: 'V', 22: 'W', 23: 'X',
         24: 'Y', 25: 'Z'}

freq = {'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043,
        'E': 0.127, 'F': 0.022, 'G': 0.020, 'H': 0.061,
        'I': 0.070, 'J': 0.002, 'K': 0.008, 'L': 0.040,
        'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019,
        'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091,
        'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001,
        'Y': 0.020, 'Z': 0.001}

def letterToVal(letter):
    letter = letter.upper()
    return vals[letter]

def valToLetter(val):
    return nums[val]

def getSq(s):
    expCount=dict.fromkeys(range(26), 0)
    chiSq=0
    for y in range(26):
        expCount[y]=freq[valToLetter(y)]*len(s)

    for y in range(26):
            chiSq= chiSq+(((s.count(valToLetter(y))-expCount[y])**2)/expCount[y])

    return chiSq

def getKeyLetter(c):
    return valToLetter((min(c, key=lambda k: c[k])))

def decrypt(c, k):
    output = ''
    keyIndex = 0
    for x in c:
        output = output + valToLetter((letterToVal(x)-letterToVal(k[keyIndex]))%26)
        if keyIndex == len(k)-1:
            keyIndex = 0
        else:
            keyIndex = keyIndex+1

    return output

def findKey(keyLength, stripcipher):
    #Store nth letter strings in dictionary for frequency analysis
    keys = dict.fromkeys(range(keyLength),'')
    for j in range(keyLength):
        for i in range(j, len(stripcipher), keyLength):
            keys[j]=keys[j]+stripcipher[i]

    #Deciphers each letter of strings of every nth letter using each letter in the
    #alphabet. Stores output in dictionaries within masterDictionary.
    masterDictionary = {}
    for i in range(keyLength):
        masterDictionary['d'+str(i)] = dict.fromkeys(range(26), '')

    for x in range(keyLength):
        for j in range(26):
            for i in keys[x]:
                masterDictionary['d'+str(x)][j] = masterDictionary['d'+str(x)][j]+valToLetter(((letterToVal(i))-j)%26)

    #Perform Chi Square analysis on the deciphered strings and store in masterCipher
    masterCipher = {}
    for i in range(keyLength):
        masterCipher['c'+str(i)] = dict.fromkeys(range(26), '')

    for i in range(keyLength):
        for j in range(26):
            masterCipher['c'+str(i)][j] = getSq(masterDictionary['d'+str(i)][j])

    '''
    Guess secret key based on Chi Sq. Analysis and return results
    '''
    key = ''
    for i in range(keyLength):
        key = key + getKeyLetter(masterCipher['c'+str(i)])
    return key, masterCipher

'''
The following Kasiski Analysis code is modified from Invent With Python:
https://inventwithpython.com/vigenereHacker.py
'''
def findRepeatSequencesSpacings(message):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).


    # Compile a list of seqLen-letter sequences found in the message.
    seqSpacings = {} # keys are sequences, values are list of int spacings
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is, and store it in seq
            seq = message[seqStart:seqStart + seqLen]

            # Look for this sequence in the rest of the message
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # initialize blank list

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence.
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1. For example, getUsefulFactors(144)
    # returns [2, 72, 3, 48, 4, 36, 6, 24, 8, 18, 9, 16, 12]

    if num < 2:
        return [] # numbers less than 2 have no useful factors

    factors = [] # the list of factors found

    # When finding factors, you only need to check the integers up to
    # MAX_KEY_LENGTH.
    for i in range(2, MAX_KEY_LENGTH + 1): # don't test 1
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))


def getItemAtIndexOne(x):
    return x[1]


def getMostCommonFactors(seqFactors):
    # First, get a count of how many times a factor occurs in seqFactors.
    factorCounts = {} # key is a factor, value is how often if occurs

    # seqFactors keys are sequences, values are lists of factors of the
    # spacings. seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Second, put the factor and its count into a tuple, and make a list
    # of these tuples so we can sort them.
    factorsByCount = []
    for factor in factorCounts:
        # exclude factors larger than MAX_KEY_LENGTH
        if factor <= MAX_KEY_LENGTH:
            # factorsByCount is a list of tuples: (factor, factorCount)
            # factorsByCount has a value like: [(3, 497), (2, 487), ...]
            factorsByCount.append( (factor, factorCounts[factor]) )

    # Sort the list by the factor count.
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount


def kasiskiExamination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occur multiple times
    # in the ciphertext. repeatedSeqSpacings has a value like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    # See getMostCommonFactors() for a description of seqFactors.
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # See getMostCommonFactors() for a description of factorsByCount.
    factorsByCount = getMostCommonFactors(seqFactors)

    # Now we extract the factor counts from factorsByCount and
    # put them in allLikelyKeyLengths so that they are easier to
    # use later.
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths, factorsByCount

'''
Program Start
'''
#collect ciphertext from user and remove spaces and punctuation
ciphertext = input("Enter complete ciphertext: ")
exclude = set(string.punctuation)
ciphertext = ''.join(x for x in ciphertext if x not in exclude)
spaceList = []
for i in range(len(ciphertext)):
    if ciphertext[i] == ' ':
        spaceList.append(i)
stripcipher = ciphertext.replace(' ', '')
stripcipher = stripcipher.upper()

#find possible key lengths
allLikelyKeyLengths, kasiskiMaster = kasiskiExamination(stripcipher)

opt = "n"
print("Attempting decryption process using likely key lengths...")
for x in allLikelyKeyLengths:
    key, masterCipher = findKey(x, stripcipher)
    print("Found Decryption Key: " + key)
    decrypted = decrypt(stripcipher, key)
    for i in spaceList:
        decrypted = decrypted[:i] + ' ' + decrypted[i:]
    print("Decrypted Message: " + decrypted)
    display = input("Display Kasiski analysis and frequency analysis? y/n: ")
    if display == "y":
        print("Kasiski Analysis Table: ")
        print("Key Length: \t Score:")
        for x in kasiskiMaster:
            print(str(x[0]) + "\t \t" + str(x[1]))
        print("Chi Square Analysis Table given Key Length " + str(x))
        for x in masterCipher:
            print("Key Letter: "+ str(x))
            print("Letter: \t Chi Square:")
            for y in masterCipher[x]:
                print(valToLetter(y) + "\t  \t" + str(masterCipher[x][y]))

    #Check decryption, continue if incorrect
    opt = input("Is this decryption correct? y/n: ")
    if opt == "y":
        break
    else:
        print("Trying next key length...")

print("Process complete.")
