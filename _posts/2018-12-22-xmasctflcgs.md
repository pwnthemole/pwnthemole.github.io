---
title: X-MAS CTF 2018 - Let's Crack the Great(er) lapland monolith
layout: post
author: "mr96"
category: crypto
tags: crypto prng lcg
---
These are two very similar challenges: the first one has a bug so that you can solve it in an unintended way, so the organizers realized a second "fixed" challenge. The following method works for both of them.

We're given a web page that gets a random integer and asks us to guess it, multiple times. After guessing correctly 20 times, it will return a flag.

## Solution
From the title we can see that the prng is of lcg type (linear congruential generator), that is,  given 3 integers $$a,b,n$$ and a seed $$x_0$$, the sequence is constructed as $$x_i=ax_{i-1}+b \pmod{n}$$. It turns out that the website tells you what value it randomized even if you fail, so observing about 10 values we can break the prng as follows:
* Construct a sequence $$t_k=x_{k+1}-x_k=a(x_k-x_{k-1})=at_{k-1}$$
* Observe that $$s_k=t_{k+1}t_{k-1}-t_k^2 \equiv 0 \pmod{n}$$
* Retrieve $$n=gcd(s_1,s_2,...)$$
* Retrieve $$a=\frac{x_2-x_1}{x_1-x_0} \pmod{n}$$
* Retrieve $$b=x_1-ax_0 \pmod{n}$$

We did this using the Python script from msm from p4team and then did it on the website by hand (input 20 times is faster than scripting). Here's the code:
```
from functools import reduce
from gmpy2 import gcd

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)

obs = [9933, 16949, 696, 30323, 33563, 25061, 14546, 13243, 12116]

n,k,d = crack_unknown_modulus(obs)
state = obs[-1]

while True:
    state = (state*k+d) % n
    print(state)
    input()

```
