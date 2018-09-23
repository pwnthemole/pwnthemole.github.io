---
title: CSAW CTF Quals 2018 - Take an L Writeup
layout: post
author: "mr96"
category: misc
tags: misc math divide_et_impera
---

This task is not a common CTF problem, but a very well-known math olympiads and informatics olympiads problem. It's not very difficult, but I'm doing this writeup because I think it's one of the problems you have to know before any math or informatics competition.

The server says that we have a $$64 \times 64$$ grid, with one missing square, randomized every time. We have to fill this grid using only 3-square L-shaped polyominos, of course not overlapping them and using only the space in the grid.

## Problem Analysis
We'll now prove the following: let $$n\geq 1$$ be a positive integer, then every $$2^n \times 2^n$$ grid with one missing square can be tiled using only 3-square L-shaped polyominos.

*Proof: let's prove this by induction: for $$n = 1$$ trivially we can just use one polyomino and cover the remaining 3 squares. So assuming it works for $$n$$ let's prove it for $$n+1$$: without loss of generality we can assume that the missing square lies in the portion of grid between $$(0,0)$$ (we're labeling the squares from top left) and $$(2^n-1,2^n-1)$$ (otherwise we can just rotate the grid) so filling with one polyomino the squares labeled $$(2^n-1,2^n)$$, $$(2^n,2^n)$$ and $$(2^n,2^n-1)$$ and cutting the grid in four parts we obtain 4 different grids $$2^n\times 2^n$$ with one missing square, and so by the inductive hypothesis we are done.*

## Solution
Why have we proven that result? Because the algorithm used in the proof is our solution! We just have to implement it recursively and we are done. The following Python script does the job:

```
from pwn import *

def fill(dim,pos1,pos2,start1,start2):
    global r
    pos = 0
    a = ""
    if dim < 2:
        return
    if pos1>=start1+dim/2:
        if pos2>=start2+dim/2:
            pos = 4
        else:
            pos = 3
    else:
        if pos2>=start2+dim/2:
            pos = 2
        else:
            pos = 1
    if pos == 1:
        a += "("+str(start1+dim//2-1)+","+str(start2+dim//2)+"),("+str(start1+dim//2)+","+str(start2+dim//2)+"),("+str(start1+dim//2)+","+str(start2+dim//2-1)+")"
        print(a)
        r.sendline(a)
        fill(dim//2,pos1,pos2,start1,start2)
        fill(dim//2,start1+dim//2-1,start2+dim//2,start1,start2+dim//2)
        fill(dim//2,start1+dim//2,start2+dim//2-1,start1+dim//2,start2)
        fill(dim//2,start1+dim//2,start2+dim//2,start1+dim//2,start2+dim//2)
    elif pos == 2:
        a += "("+str(start1+dim//2-1)+","+str(start2+dim//2-1)+"),("+str(start1+dim//2)+","+str(start2+dim//2-1)+"),("+str(start1+dim//2)+","+str(start2+dim//2)+")"
        print(a)
        r.sendline(a)
        fill(dim//2,start1+dim//2-1,start2+dim//2-1,start1,start2)
        fill(dim//2,pos1,pos2,start1,start2+dim//2)
        fill(dim//2,start1+dim//2,start2+dim//2-1,start1+dim//2,start2)
        fill(dim//2,start1+dim//2,start2+dim//2,start1+dim//2,start2+dim//2)
    elif pos == 3:
        a += "("+str(start1+dim//2-1)+","+str(start2+dim//2-1)+"),("+str(start1+dim//2-1)+","+str(start2+dim//2)+"),("+str(start1+dim//2)+","+str(start2+dim//2)+")"
        print(a)
        r.sendline(a)
        fill(dim//2,start1+dim//2-1,start2+dim//2-1,start1,start2)
        fill(dim//2,start1+dim//2-1,start2+dim//2,start1,start2+dim//2)
        fill(dim//2,pos1,pos2,start1+dim//2,start2)
        fill(dim//2,start1+dim//2,start2+dim//2,start1+dim//2,start2+dim//2)
    else:
        a += "("+str(start1+dim//2-1)+","+str(start2+dim//2)+"),("+str(start1+dim//2-1)+","+str(start2+dim//2-1)+"),("+str(start1+dim//2)+","+str(start2+dim//2-1)+")"
        print(a)
        r.sendline(a)
        fill(dim//2,start1+dim//2-1,start2+dim//2-1,start1,start2)
        fill(dim//2,start1+dim//2-1,start2+dim//2,start1,start2+dim//2)
        fill(dim//2,start1+dim//2,start2+dim//2-1,start1+dim//2,start2)
        fill(dim//2,pos1,pos2,start1+dim//2,start2+dim//2)
    #print(r.recvline())
r = remote('misc.chal.csaw.io',9000)
r.recvuntil("block: ")
s = r.recvline()
pos = str(s).split(",")
pos[0] = int(pos[0][3:])
pos[1] = int(pos[1].lstrip()[:2].rstrip(')'))
fill(64,pos[0],pos[1],0,0)
print(s,pos)
print(r.recvline())

```
and we can find the flag `flag{m@n_that_was_sup3r_hard_i_sh0uld_have_just_taken_the_L}`
