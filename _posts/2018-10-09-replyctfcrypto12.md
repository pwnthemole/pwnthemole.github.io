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
What we have to do now is to reconstruct the original file starting from the last 65 bytes and knowing that part of these bytes are also in the key.

```
import gmpy2
from Crypto.PublicKey import RSA

e = 65537L
n = 16809924442712290290403972268146404729136337398387543585587922385691232205208904952456166894756423463681417301476531768597525526095592145907599331332888256802856883222089636138597763209373618772218321592840374842334044137335907260797472710869521753591357268215122104298868917562185292900513866206744431640042086483729385911318269030906569639399362889194207326479627835332258695805485714124959985930862377523511276514446771151440627624648692470758438999548140726103882523526460632932758848850419784646449190855119546581907152400013892131830430363417922752725911748860326944837167427691071306540321213837143845664837111L
p = 0

for k in range(int(e/2),e):
    delta = 1+4*k*n*e
    if gmpy2.is_square(delta):
        y = gmpy2.isqrt(delta)
        if (y-1)%(2*k) == 0:
            p1 = (y-1)/(2*k)
            if n%p1 == 0:
                print("Found!")
                p = p1
                break

q = n/p
phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)
key = RSA.construct((n,e,long(d)))
data = open('revolutional-secure-angou/flag.encrypted', 'r').read()
print(key.decrypt(data))
```
and we can find the flag `TWCTF{9c10a83c122a9adfe6586f498655016d3267f195}`
