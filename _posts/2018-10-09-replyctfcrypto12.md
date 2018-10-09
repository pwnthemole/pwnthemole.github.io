---
title: Reply CTF 2018 - Crypto1 & Crypto2 Writeup
layout: post
author: "mr96"
category: crypto
tags: crypto rsa xor rot-13 classic
---
# Crypto1 - RoXor (100 pt.)
We're given a Python code and a file `TOP_secret.zip.enc`
```
#!/usr/bin/python2.7

import hashlib, base64, sys


def decriptMe():
    with open("TOP_secret.zip.enc") as f:
        return f.read()

def encryptionKey(k):
    m = hashlib.md5()
    m.update(k)
    key = m.hexdigest()
    return key

def decryption(key, cyphertext):
    plaintext = ""
    k = 0
    for i in base64.b64decode(cyphertext):
        p = ord(key[k]) ^ ord(i)
        plaintext = plaintext + chr(p)
        key += chr(p)
        k += 1
    return plaintext

def encryption(plaintext):
    key = encryptionKey("key")
    print "[*] Key: {}\n[*] Plaintext: {}".format(key, str(len(plaintext)))
    cyphertext = ""
    for i in xrange(len(plaintext)):
        c = (ord(key[i]) ^ ord(plaintext[i]))
        cyphertext = cyphertext + chr(c)
        key += plaintext[i]
    return base64.b64encode(cyphertext)

def check(plaintext):
    if plaintext[-65:] == "6c81d06ac6d2709a81f76a9bf6c3f5933002f00053302447b122260a0ac0c18e\n":
        return True
    return False

def main(key):
    enkey = encryptionKey(key)
    print "[*] Key Encrypted: %s" % (enkey)
    plaintext = decryption(enkey, decriptMe())
    print plaintext[-65:]
    if check(plaintext):
        print "[*] Key Correct! Plaintext:\n %s" % (plaintext)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print 'Give me the key\n Example: %s key' % (sys.argv[0])
        exit(1)
    main(sys.argv[1])
```

## Code Analysis
* The function `decriptMe` simply opens the encrypted file and return its content.
* The function `encryptionKey` generates the md5 hash of the key `k` given in input.
* The function `decryption`, given a key and the ciphertext, gives back the plaintext. Observe that every recovered character is added at the end of the key and is reused 32 charaters later. Noticed this, the decryption process is a simple xor, as the title of the challenge suggests.
* The function `encryption` does exactly what it is supposed to do. The only interesting part is that it uses as a key the md5 hash of the real key, then the process is the same as the decryption one.
* The function `check` checks if the file has been decrypted correctly, comparing the last 65 bytes with the last 65 bytes of the real file (as a string in the source). Here is the weakness of the cryptosystem.

## Attack
What we have to do now is to reconstruct the original file starting from the last 65 bytes and knowing that part of these bytes are also in the key so, basically, we have to do in reverse the encryption process:

```
def solve():
    cipher = b64decode(decriptMe())
    plaintext = "6c81d06ac6d2709a81f76a9bf6c3f5933002f00053302447b122260a0ac0c18e\n"
    key = "6c81d06ac6d2709a81f76a9bf6c3f5933"
    for i in cipher[:-len(key)]:
        p = ord(plaintext[-len(key)-1]) ^ ord(cipher[-len(key)-1])
        plaintext = chr(p) + plaintext
        key = chr(p) + key
    return key[:32]
```
the function returns `9dc5616a9df448ce476be9d8dd638a9c`; calling the decryption function with this key and redirecting the result to a file gives a zip which, when extracted, gives a text file with the flag: `{FLG:Y0yNe3dT0goD33peR!}`

# Crypto 2 - Something is missing (200 pt.)
In this challenge we are only given a file, without any explanation. The file contains some encrypted data and, using hexeditor, we can see that there are a lot of zeros at the beginning of the file. After some time the organizers gave us an hint: the file is encrypted using RSA. Since we have no informations or public key we assume that the attack does not depend on the modulus: the simpler attack is supposing that the file has been encrypted with $e=3$ and a very large modulus, so taking the cube root will basically give us the flag.

```
from Crypto.Util.number import bytes_to_long
from binascii import unhexlify

def long_to_bytes (val, endianness='big'):
    width = val.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % val)
    if endianness == 'little':
        s = s[::-1]
    return s

def cube_root(n):
    lo = 0
    hi = n
    while lo < hi:
        mid = (lo + hi) // 2
        if mid**3 < n:
            lo = mid + 1
        else:
            hi = mid
    return lo

r = open("encrypted", "r").read()
r_num = bytes_to_long(r)
sqrt3 = cube_root(r_num)
print(long_to_bytes(sqrt3))
```
The script returns `}!Erc33Qre0Z:TYS{ :ryvs CVM rug ebs qrra hbl qebjffnc rug fv fvuG`: reverting the string and decrypting with `rot-13` gives the flag `{FLG:M0reD33peR!}`.
