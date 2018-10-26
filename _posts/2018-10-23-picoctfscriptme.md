---
title: picoCTF 2018 - Script Me Writeup
layout: post
author: "matpro98"
category: misc
tags: misc python regex pwntools
---

We can connect to the challenge via the command `nc 2018shell2.picoctf.com 7866`, getting this:

```
Rules:
() + () = ()()                                      => [combine]
((())) + () = ((())())                              => [absorb-right]
() + ((())) = (()(()))                              => [absorb-left]
(())(()) + () = (())(()())                          => [combined-absorb-right]
() + (())(()) = (()())(())                          => [combined-absorb-left]
(())(()) + ((())) = ((())(())(()))                  => [absorb-combined-right]
((())) + (())(()) = ((())(())(()))                  => [absorb-combined-left]
() + (()) + ((())) = (()()) + ((())) = ((()())(())) => [left-associative]

Example: 
(()) + () = () + (()) = (()())

Let's start with a warmup.
()() + (()(())) = ???
```

The brackets groups act like cells, and the bigger cell "eats" the smaller one. Understanding this, we can write a simple Python script which parses the expression, finds the answer and eventually prints the flag.
The code is this:

```
from pwn import *
import re

r=remote('2018shell2.picoctf.com',7866)

def parse(s):
    arr=s.split('+')
    return arr

def size(s):
    m=0
    count=0
    for i in range(len(s)):
        if s[i]=='(':
            count+=1
        elif s[i]==')':
            m=max(m,count)
            count-=1
    return m

def answer(arr,s1):
    for i in range(len(arr)-1):
        if size(s1)>size(arr[i+1]):
            s1=s1[:-1]+arr[i+1]+')'
        elif size(s1)==size(arr[i+1]):
            s1=s1+arr[i+1]
        else:
            s1='('+s1+arr[i+1][1:]
    return s1

s=''
while 'flag' not in s:
    while '???' not in s and 'flag' not in s:
        s=r.recvline()
    if '???' in s:
        s=re.sub('[^()+]','',s)
        arr=parse(s)
        s1=arr[0]
        s1=answer(arr,s1)
        r.send(s1+'\n')
    else:
        print(s)
        r.close()
```

And the output is:

```
[+] Opening connection to 2018shell2.picoctf.com on port 7866: Done
Congratulations, here's your flag: picoCTF{5cr1pt1nG_l1k3_4_pRo_45ca3f85}

[*] Closed connection to 2018shell2.picoctf.com port 7866
```

So the flag is `picoCTF{5cr1pt1nG_l1k3_4_pRo_45ca3f85}`.
