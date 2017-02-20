# python-vigenere
Python program that recovers the 5-character key of a message encrypted with the Vigenere cipher using Chi-Sq analysis.

This program recovers the key of a message encrypted using the Vigerene Cipher
and an assumed key length of 5. The key is recovered using a Chi-Square to perform
frequency analysis on the message as compared to a frequency table of letters in
the English language. As such, the first key recovered may not accurately decrypt the
message. The program can display a Chi-Sq. table for each potential key letter in 
the event that decryption fails. If the generated key does not decrypt the message, 
please use the key letter with the next lowest Chi-Sq. value to decrypt.

# Usage:
Run in any Python 2.x shell

At a terminal prompt:
user$ python vigenere.py
