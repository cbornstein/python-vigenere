'''
Clare Bornstein

This program recovers the key of a message encrypted using the Vigerene Cipher
and an assumed key length of 5. The key is recovered using a Chi-Square to perform
frequency analysis on the message as compared to a frequency table of letters in
the English language. As such, the key recovered may not be the actual key. The
program can display a Chi-Sq. table for each potential key letter in the event that
decryption fails. If the generated key does not decrypt the message, please use
the key letter with the next lowest Chi-Sq. value to decrypt.


Frequency of Letters in English Language from Wikipedia:
https://en.wikipedia.org/wiki/Letter_frequency
'''

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
    return vals[letter]

def valToLetter(val):
    return nums[val]

def getSq(s):
    expCount=dict.fromkeys(range(26), 0)
    chiSqr=0
    for y in range(26):
        expCount[y]=freq[valToLetter(y)]*len(s)

    for y in range(26):
            chiSqr= chiSqr+(((s.count(valToLetter(y))-expCount[y])**2)/expCount[y])

    return chiSqr

def getKeyLetter(c):
    return valToLetter((min(c, key=lambda k: c[k])))

def decrypt(c, k):
    output=''
    keyIndex=0
    for x in c:
        output = output + valToLetter((letterToVal(x)-letterToVal(k[keyIndex]))%26)
        if keyIndex == len(k)-1:
            keyIndex = 0
        else:
            keyIndex=keyIndex+1

    return output
        

#remove spaces and punctuation

ciphertext = input("Enter complete ciphertext: ")
stripcipher = ciphertext.replace(' ', '')
stripcipher = stripcipher.replace(',', '')
stripcipher = stripcipher.replace('.', '')

#print(stripcipher)


#Dictionary to store every nth letter strings

keys = dict.fromkeys(range(5),'')

for j in range(5):
    for i in range(j, len(stripcipher), 5):
        keys[j]=keys[j]+stripcipher[i]

#print(keys)

d0 = dict.fromkeys(range(26), '')
d1 = dict.fromkeys(range(26), '')
d2 = dict.fromkeys(range(26), '')
d3 = dict.fromkeys(range(26), '')
d4 = dict.fromkeys(range(26), '')

'''
Deciphers each letter of strings of every nth letter using each letter in the
alphabet. Stores output in dictionaries.
'''

#d0
for j in range(26):
    for i in keys[0]:
        d0[j]=d0[j]+valToLetter(((letterToVal(i))-j)%26)

#print(d0)

#d1
for j in range(26):
    for i in keys[1]:
        d1[j]=d1[j]+valToLetter((letterToVal(i)-j)%26)

#print(d1)

#d2
for j in range(26):
    for i in keys[2]:
        d2[j]=d2[j]+valToLetter((letterToVal(i)-j)%26)

#print(d2)

#d3
for j in range(26):
    for i in keys[3]:
        d3[j]=d3[j]+valToLetter((letterToVal(i)-j)%26)

#print(d3)

#d4
for j in range(26):
    for i in keys[4]:
        d4[j]=d4[j]+valToLetter((letterToVal(i)-j)%26)

#print(d4)

c0 = dict.fromkeys(range(26), '')
c1 = dict.fromkeys(range(26), '')
c2 = dict.fromkeys(range(26), '')
c3 = dict.fromkeys(range(26), '')
c4 = dict.fromkeys(range(26), '')

'''
Performs Chi Square analysis on the deciphered strings and stores them in a dictionary
'''
for j in range(26):
    c0[j]=getSq(d0[j])
    
#print(c0)

for j in range(26):
    c1[j]=getSq(d1[j])

#print(c1)

for j in range(26):
    c2[j]=getSq(d2[j])

#print(c2)

for j in range(26):
    c3[j]=getSq(d3[j])

#print(c3)

for j in range(26):
    c4[j]=getSq(d4[j])

#print(c4)

'''
Guess secret key based on Chi Sq. Analysis
'''
key = getKeyLetter(c0)
key = key + getKeyLetter(c1)
key = key + getKeyLetter(c2)
key = key + getKeyLetter(c3)
key = key + getKeyLetter(c4)

print("The decryption key is: " + key)
str = input("Attempt decryption with recovered key? y/n: ")
if(str =="y"):
    print(decrypt(stripcipher, key))
    print("Decryption complete.")

else:
    str = input("Would you like to select a different key using Chi Square Tables? y/n: ")
    if(str =="y"):
        print(c0, c1, c2, c3, c4)
        print("Each number corresponds to its sequential number in the alphabet, with A=0 and Z=25")
        str = input("Please enter key to decrypt. Key must be 5 characters in length: ")
        if(len(str)!=5):
            print("Incorrect key length. Message not decrypted.")
        else:
            print(decrypt(stripcipher, str))
    else:
        print("Message not decrypted.")
        
