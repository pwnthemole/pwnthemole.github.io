---
title: SecurinetsCTF 2019  - RSA/Encoding Error Writeup
layout: post
author: "mr96"
category: crypto
tags: crypto rsa error
---
# RSA/Encoding Error (1000 pts., 6 solves)
We're given a zip file in which we can find a png image. The image looks like a QR code but the dimensions are $$887 \times 521$$. Resizing the image and using a QR scanner we can find the text `Hint: every information counts`. Running `binwalk -e ctf_image.png` we can find a file named `output.txt`. Looking into the file we can see that every line is formed by sequences of 0 and 1 and every 5 bits there is a dot. Using the title we recognize this as an error correction code, so, basically, every sequence of 5 bits represents a single bit: to prevent errors the same bit is transmitted 5 times, so if in the sequence there are more 1s than 0s the bit was most likely a 1 and viceversa.

Now we look to the other part of the title: RSA. Looking with hexeditor the QR we can find a comment that says $$e=65537$$, so we have the exponent, but what about the modulus? Recalling the hint we found in the QR and that we need two prime numbers for the modulus, we find that the dimensions of the original QR are two primes! So basically we are done. Here's the python script to complete the challenge.
```
from Crypto.Util.number import inverse, long_to_bytes

p = 887
q = 521
e = 65537
n = 887*521
phi = (p-1)*(q-1)
d = inverse(e,phi)

lines = [line.rstrip('\n') for line in open('output.txt')]
#print(lines)

for l in lines:
    c = l.split(".")
    cipher=""
    for cc in c:
        if cc.count("0")>cc.count("1"):
            cipher = cipher + "0"
        else:
            cipher = cipher + "1"
    print(long_to_bytes(pow(int(cipher,2),d,n)).decode(), end="")
```

And so we obtain the flag: `Securinets{xJbht0oWpsOa1e3WnXo9FDnUj3VZpZsuxMPVlYEN}`
