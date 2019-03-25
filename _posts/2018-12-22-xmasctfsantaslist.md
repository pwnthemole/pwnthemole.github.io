---
title: X-MAS CTF 2018 - Santa's List 1 & 2 Writeup
layout: post
author: "mr96"
category: crypto
tags: crypto rsa
---
These two challenge are very similar: the only difference is that in the first one we can do how many requests we want to the server, while in the second one we are limited to 5 requests. We'll treat only the second, showing a solution that works in 4 requests.<br/>
We're given the Python code used on the server:
```
#!/usr/bin/python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

FLAG = open('flag.txt', 'r').read().strip()

def menu():0
    print()
    print('[1] Encrypt')
    print('[2] Decrypt')
    print('[3] Exit')
    return input()


def encrypt(m):
    return pow(m, rsa.e, rsa.n)


def decrypt(c):
    return pow(c, rsa.d, rsa.n)


rsa = RSA.generate(1024)
flag_encrypted = pow(bytes_to_long(FLAG.encode()), rsa.e, rsa.n)
used = [bytes_to_long(FLAG.encode())]

print('Ho, ho, ho and welcome back!')
print('Your list for this year:\n')
print('Sarah - Nice')
print('Bob - Nice')
print('Eve - Naughty')
print('Galf - ' + hex(flag_encrypted)[2:])
print('Alice - Nice')
print('Johnny - Naughty')

for i in range(5):
    choice = menu()

    if choice == '1':
        m = bytes_to_long(input('\nPlaintext > ').strip().encode())
        used.append(m)

        print('\nEncrypted: ' + str(encrypt(m)))

    elif choice == '2':
        c = int(input('\nCiphertext > ').strip())

        if c == flag_encrypted:
            print('Ho, ho, no...')

        else:
            m = decrypt(c)

            for no in used:
                if m % no == 0:
                    print('Ho, ho, no...')
                    break

            else:
                print('\nDecrypted: ' + str(m))

    elif choice == '3':
        print('Till next time.\nMerry Christmas!')
        break

print('Too many requests made... Disconnecting...')
```
## Code Analysis
The code looks very simple, basically we're given the encrypted flag, encrypted with a secure RSA key with the standard $$e=65537$$ exponent (as it is not specified when creating the key). We can encrypt whatever we want, but we can't decrypt things that, when decrypted, are multiples of the flag or multiples of the things we've encrypted.

## Attack
The first thing is to recover the modulus $$n$$: suppose we encrypt two different integers $$x_1,x_2$$ obtaining $$c_1,c_2$$, then we have that
$$x_1^e-c_1 \equiv x_2^e-c_2 \equiv 0 \pmod{n}$$

and so $$gcd(x_1^e-c_1,x_2^e-c_2)=kn$$, most likely with $$k=1$$ if we choose the integers such that $$gcd(x_1,x_2)=1$$.

Once we recovered $$n$$ the rest is trivial: take the least prime $$p$$ such that it divides the decrypted flag (I'm lazy so I waited for it to be equal to 2), so we have

$$D(flag\cdot 2^{-1})=flag\cdot 2^{-d}$$

then simply decrypt 2 to get $$D(2)=2^d$$ and multiply it with the previous result to get the decimal value of the flag. Use whatever `long_to_bytes` function to get the string.

Here's the Python code for the attack, I did the last part by hand using the interactive mode from pwntools, the script simply recovers $$n$$.
```
from pwn import *
import gmpy2
from Crypto.Util.number import *

v1 = 2
v2 = 3

r = remote("199.247.6.180", 16002)
r.recvuntil("Galf - ")
flag = int(r.recvline().decode().rstrip("\n"),16)
print(flag)
for _ in range(6):
    print(r.recvline())
r.sendline("1")
r.recvuntil(">")
r.sendline(chr(v1))
print(r.recvuntil("Encrypted: "))
c1 = int(r.recvline().decode().rstrip("\n"))
r.recvuntil("Exit\n")
r.sendline("1")
r.recvuntil(">")
r.sendline(chr(v2))
print(r.recvuntil("Encrypted: "))
c2 = int(r.recvline().decode().rstrip("\n"))
r.recvuntil("Exit\n")
n = gmpy2.gcd(v2 ** 65537 - c2, v1 ** 65537 - c1)
assert pow(v1, 65537, n) == c1
r.sendline("2")
r.recvuntil(">")
assert flag % 2 == 0
to_send = flag//2
print(to_send)
r.interactive()
```

## Bonus
The modulus can be recovered with only one request, that is

$$D(-1)\equiv n-1 \pmod{n}.$$

The flag can be also recovered with only one requests, but this is a little bit trickier and left to the reader :) simply notice that, with this method, we  only need 2 requests!
