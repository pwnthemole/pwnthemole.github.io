---
title: X-MAS CTF 2018 - X^n-MAS Writeup
layout: post
author: "mr96"
category: crypto
tags: crypto polynomials
---
For this challenge we're only given a netcat connection and the following description:

*Crypto mecha gnomes love random polynomial functions, can you guess what’s hidden in there?*

## Solution
Connecting to netcat we're given a modulus and the possibility to evaluate a polynomial at 50 points. The first thing that comes in mind is interpolation: we can retrieve the whole polynomial if the degree is at most 49 (spoiler: it is). In order to do this we use Lagrange's interpolation method, that basically is: given $$(x_0,y_0),...,(x_n,y_n)$$, then the interpolation polynomial in Lagrange's form is

$$L(x)=\sum_{j=0}^n y_j\prod_{m \neq j} \frac{x-x_m}{x_j-x_m}.$$

Basically all works also with polynomials in the $$\mathbb{Z}_n[x]$$ ring. Fortunately, we found out that one of the organizers (Gabies) has, on his github page, a class to work with polynomials in $$\mathbb{Z}_n[x]$$, so using his code we can do the following script to obtain the flag:
```
from pwn import *
from Crypto.Util.number import inverse

xy = []

class Polynomial(list):

    def __init__(self,coeffs):
        self.coeffs = coeffs

    def evaluate(self,x,mod):
        val = 0
        for i in range(len(self.coeffs)):
            val = (val + x**i * self.coeffs[i]) % mod
        return val

    def raise_degree(self,x):
        coeffs=[]

        for i in range(x):
            coeffs.append(0)
        for i in range(len(self.coeffs)):
            coeffs.append(self.coeffs[i])
        self.coeffs=coeffs

    def add_to_degree(self,x,y):
        while(len(self.coeffs)<=x):
            self.coeffs.append(0)
        self.coeffs[x]=(self.coeffs[x]+y)%MOD

    def add_poly(self,x):
        while(len(self.coeffs)<len(x.coeffs)):
            self.coeffs.append(0)

        for i in range(len(x.coeffs)):
            self.coeffs[i]=(self.coeffs[i]+x.coeffs[i])%MOD

    def multiply(self,x):
        for i in range(len(self.coeffs)):
            self.coeffs[i]=(self.coeffs[i] * x)%MOD

    def multiply_with_poly(self,p):
        coeffs=Polynomial([])

        for i in range(len(self.coeffs)):
            q=Polynomial(p.coeffs)
            q.raise_degree(i)
            q.multiply(self.coeffs[i])
            coeffs.add_poly(q)
        self.coeffs=coeffs.coeffs

    def calculate_derivative(self):
        p=Polynomial([])
        for i in range(1,len(self.coeffs)):
            p.coeffs.append((self.coeffs[i]*i)%MOD)
        return p

    def compose(self,p):
        P=Polynomial([])
        q=Polynomial([1])
        for i in range(len(self.coeffs)):
            q2=Polynomial(q.coeffs)
            q2.multiply(self.coeffs[i])
            P.add_poly(q2)
            q.multiply_with_poly(p)
        self.coeffs=P.coeffs

    def print_poly(self):
        return self.coeffs

#Lagrange Interpolation part
def Lagrange_Basis_Polynomial(xlist,index):
    l=Polynomial([1])
    for i in range(len(xlist)):
        if(i==index):
            continue
        p=Polynomial([(MOD-xlist[i])%MOD,1])
        p.multiply(inverse((MOD+xlist[index]-xlist[i])%MOD,MOD))
        l.multiply_with_poly(p)
    return l

def Lagrange_Polynomial(xylist):
    xlist=[]
    ylist=[]
    L=Polynomial([])
    for a in xylist:
        xlist.append(a[0])
        ylist.append(a[1])
    for i in range(len(ylist)):
        l=Lagrange_Basis_Polynomial(xlist,i)
        l.multiply(ylist[i])
        L.add_poly(l)
    return L

r = remote("199.247.6.180", 16000)
r.recvuntil("modulo is ")
n = int(r.recvline().decode().split(".")[0])
print(n)
MOD = n
for i in range(50):
    r.recvuntil(":")
    r.sendline(str(i))
    t = int(r.recvline().decode().split(":")[1].rstrip("\n").lstrip(" "))
    print((i,t))
    xy.append((i,t))
print(xy)
coeffs = Lagrange_Polynomial(xy).print_poly()
print(coeffs)
c = ""
for i in range(len(coeffs)):
    print(chr(coeffs[49-i]), end="")

```
