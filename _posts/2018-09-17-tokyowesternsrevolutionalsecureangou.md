---
title: Tokyo Westerns CTF 2018 - Revolutional Secure Angou Writeup
layout: post
author: "mr96"
tags: crypto rsa
category: crypto
---

We're given a short Ruby code used to encrypt the flag, the public key and the encrypted flag.
```
require 'openssl'

e = 65537
while true
  p = OpenSSL::BN.generate_prime(1024, false)
  q = OpenSSL::BN.new(e).mod_inverse(p)
  next unless q.prime?
  key = OpenSSL::PKey::RSA.new
  key.set_key(p.to_i * q.to_i, e, nil)
  File.write('publickey.pem', key.to_pem)
  File.binwrite('flag.encrypted', key.public_encrypt(File.binread('flag')))
  break
end
```

## Code Analysis
The code is a simple textbook RSA implementation, the only difference is that we have $$q \equiv e^{-1} \pmod{p}$$, and this is the vulnerability.

## Attack
From $$q \equiv e^{-1} \pmod{p}$$ we can write $$qe=1+kp$$ for some $$k \in \mathbb{Z}$$ and then $$kp^2+p-ne=0$$. So we have to find such $$k$$; rewriting $$k = \frac{qe-1}{p}\sim\frac{q}{p}e$$ we can see that $$k\in [\min{\frac{q}{p}e-1},\max{\frac{q}{p}e}]$$. Because $$q\in \mathbb{Z_p}$$ we have $$\frac{q}{p}< 1$$ and running

`openssl rsa -pubin -in publickey.pem  -text -noout`

we can see $$n\sim 2048$$ bits, so because $$p\sim 1024$$ bits also $$q\sim 1024$$ bits and $$\frac{q}{p}\geq \frac{1}{2}$$. Now we only have to check the values of $$k$$ from $$\frac{1}{2}e-1$$ to $$e$$ and then decrypt the flag (in less than 3 seconds with the following script).

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
