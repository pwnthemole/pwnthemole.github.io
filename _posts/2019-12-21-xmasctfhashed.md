---
title: X-MAS CTF 2019 - Hashed Presents v1 & v2 Writeup
layout: post
author: "mr96"
category: crypto
tags: crypto lattice
---
These two challenges were almost the same, so I'm doing the writeup together. In reality the first one was a lot more solved since it has an unintended vulnerability using the fact that the step value was an even number, but since the indended solution is necessary to solve the v2 we'll ignore this.
## Hashed Presents v1 (25 solves)
We have to generate 10 collisions to a custom hash function that works like this
```
class secureHash(object):
    def __init__(self):
        self.bits = 128
        self.mod = 2**128
        self.mask = 2**128 - 1
        self.step = 23643483844282862943960719738L
        self.hash = 9144491976215488621715609182563L

    def update(self, inp):
        for ch in inp:
            self.hash = ((self.hash + ord(ch)) * self.step) & self.mask

    def hexdigest(self):
        x = self.hash
        out = ''
        for i in range(self.bits/8):
            out=hex(x & 0xff)[2:].replace('L','').zfill(2)+out
            x >>= 8
        return out
```

So basically we have that given a string $$a_{n}a_{n-1}...a_2a_1$$ where the $$a_i$$'s are digits (in their decimal representation) the hash function computes $$Hs^n+a_ns^n+...+a_1s\equiv h \pmod{2^{128}}$$ where $$s$$ is the step value in the code and $$H$$ is the hash value. The idea here is pretty simple: we want to find some $$k\le n$$ such that there exists a string $$e_ke_{k-1}...e_1$$ such that $$\sum e_is^{i}\equiv 0 \pmod{2^{128}}$$ and such that the $$e_i$$ are small enough to keep $$a_i+e_i$$ a valid character. If we do this, we'll have that $$Hs^n+a_ns^n+...+(a_k+e_k)s^k+...+(a_1+e_1)s\equiv h \pmod{2^{128}}$$ and so we'll have a collision string made by the string $$a_n...(a_k+e_k)...(a_1+e_1)$$. So, how we can construct this vector? The easiest method (or, at least, the standard one) as far as i know is using the Lenstra-Lenstra-Lovász lattice basis reduction algorithm. I don't want to go into the details of the algorithm (since it's pointless here and it's already implemented in Sagemath), but basically given a basis of a lattice $$L$$ in $$\mathbb{R}^n$$ the algorithm gives you another basis that is short and nearly orthogonal in polynomial time. So, everything we need to do is to setup a basis for our lattice and then apply LLL. I choose the easiest base and setup the matrix in the following way

$$\begin{pmatrix}
1 & 0 & 0 & ... & s^k\\
0 & 1 & 0 & ... & s^{k-1} \\
0 & 0 & 1 & ... & s^{k-2}\\
\vdots & \vdots & \vdots & \ddots & s^k\\
0 & 0 & 0 & ... & t\cdot2^{128}
\end{pmatrix}$$
where $$k=30$$ (since the length of the given strings varies from 30 to 35) and $$t$$ is a parameter that we can let vary over the integers. So we generate some vectors like this from this matrix and we're done, eventually trying to sum up the $$a_i$$'s with different values of the $$e_i$$'s in order to match some.
```
mod = 2^128
n = 30
s = 23643483844282862943960719738

for t in range(1,50):
    #print(t)
    A = [[0 for i in range(n+1)] for i in range(n+1)]
    A[0][n] = mod * t
    for i in range(1,n+1):
        A[i][n] = power_mod(s,(n - i),mod)
        A[i][i-1] = 1

    A=Matrix(A)
    A=A.LLL()
    for i in range(n+1):
        if A[i][n] == 0 and A[i][n-1] == 0:
            print(A[i])
```

## Hashed Presents v2 (8 solves)
The problem here is quite similar, the only differences are: now the step is an odd number, and that there is a xor instead of an addition in the `update` function
```
class secureHash(object):
    def __init__(self):
        self.bits = 128
        self.mod = 2**128
        self.mask = 2**128 - 1
        self.step = 23643483844282862943960719737L
        self.hash = 9144491976215488621715609182563L

    def update(self, inp):
        for ch in inp:
            self.hash = ((self.hash ^ ord(ch)) * self.step) & self.mask

    def hexdigest(self):
        x = self.hash
        out = ''
        for i in range(self.bits/8):
            out=hex(x & 0xff)[2:].replace('L','').zfill(2)+out
            x >>= 8
        return out
```

So, what's changes with the xor? From the theoretical point of view, almost nothing. In fact we can reconduct the first problem to the second one very easily: suppose that we have a collision for the first cipher $$a_n...a_1$$ and $$b_n...b_1$$, then calling $$h_i$$ the value of $$h$$ after the $$i-$$th addition in the update function (i.e. when we are processing the $$(n-i)-$$th character), then since $$0<a_i<256$$ we can easily find a vector $$c_n...c_1$$ such that $$h_i+a_{n-i}=h_i\oplus c_{n-i}$$ and do the same with $$b_i$$ and $$d_i$$, obtaining a collision for the second hash function. So our strategy will be:
* Finding a string that matches the hash of the given string but for the other hash function
* Finding a collision on the first hash function
* Retrieving the collision for the second hash function using the collision on the first one
So that's the end, right? No.

The problem here is that this method in general generates a collision, but we've no control on the size of the components of this collision (and, in general, we'll have something that is 400+ and so not an ascii character).

What we need to do is to make the collision of the first hash as small as possible. We don't care about it being positive, but we need to find a vector that is as close as possible to 0. So in practice we want to solve a Close Vector Problem in the lattice generated by our LLL vectors, and in particular we want to find the closest vector to $$a_n...a_1$$ (the vector we generated on the first point of our strategy). Since CVP is NP-Hard we're going to approximate it. As far as I know the best way to do this is Babai's algorithm, that is a polynomial time algorithm that works like this (in sage):
```
def Babai_closest_vector(B, target):
    M = B.LLL()
    G = M.gram_schmidt()[0]
    small = target
    for i in reversed(range(M.nrows())):
        c = ((small * G[i]) / (G[i] * G[i])).round()
        small -=  M[i] * c
    return target - small
```
where B is a basis of the chosen lattice. So now that we have a small collision for the first problem we can simply generate the collision for the second one and solve the problem.
