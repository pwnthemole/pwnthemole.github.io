---
layout: post
title: IceCTF 2018 - Twitter Writeup
author: madt1m
tags: binary-exploitation writeup icectf
---

## Introduzione

Before diving into exploit and vulnerabilities, I'll take a little time to introduce the core concepts behind the challenge. The same key concepts which made this challenge so much fun, frustrating, and wait, did I say frustrating?

The binary, _twitter_, was basically an emulator to ROMs from the past which the challenge provided us...Pong, Space Invaders and such, you know :)

A good run of reversing with IDA and some googling made me discover a whole world of passionate programmers of this language, _Chip-8_, emerged from the 70' to provide old devs and young devs a worthy way of spending a free night, and a couple beers.

And _twitter_ is just that, a Chip-8 interpreter written in c++ written by some passionate nerd :)

![AltText1](/media/images/icectftwitter_1.JPG)

So, to properly follow and reproduce the writeup, I'd encourage you to go and take a quick read of the [link-here] _Chip-8 Instruction Set_ -- I'll refer to that in what follows.

Moreover, to successfully write my custom ROM and exploit the vulnerability I used [link here] _chipper_.

## Binary Analysis

![AltText1](/media/images/icectftwitter_2.JPG)
![AltText1](/media/images/icectftwitter_3.JPG)

The binary is NX, so we need to use some ROP technique to exploit it.
With PIE option, dynamic linking, and ASLR, not a single address in memory will be loaded in a deterministic fashion. We will definitely need some leak.

## The Vulnerability

Chip-8 accesses its RAM through a dedicated register named _Index Register_, or **I**.

An 8-bit register wouldn't be enough to address the whole content of its memory, which is historically (and modern interpreters follow the same convention) large 4K, so that the _Index_ is large 16-bit -- with 4K, only 12 of which are used.

My bet was that, in our given interpreter binary, the check to avoid that _Index_ register didn't address anything larger than 4K was faulty; so I could write custom instructions to read and write from areas of memory used by the interpreter, out of the dedicated environment. A quick run with a Proof-Of-Concept ROM confirmed the vulnerability.

_overflow.asm_
```
option binary
align off

ld I, #FFF
ld v0, #42
ld v1, #4F
ld v2, #4F
ld v3, #42
ld v4, #10

(add I, v4
ld [I], v3)*a lot of times
```
Standing to the [Chip8 Instruction Set](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM), what I'm doing here is:
- Loading the index register with the highest address in memory (0xFFF);
- Loading registers v0 thru v3 with the word _BOOB_;
- Increment I by 16, and write BOOB over memory, **a lot of times**.


`./chipper overflow.rom overflow.asm`

![AltText1](/media/images/icectftwitter_4.JPG)


We basically have a **buffer overflow** here, where the buffer is represented by the 4KB allocated to the environment. Moreover, we can issue **read and write operations from arbitrary areas of memory** up to 2^16 bytes starting from the buffer.


## The Exploit

Again, we need a leak.
But really, when you have the chance to write and read an arbitrary number of times to/from memory, you will pretty much always find something to make good use of.

![AltText1](/media/images/icectftwitter_5.JPG)

My strategy here was:
- Examine saved return addresses with _backtrace_;
- Search in memory to find where they are stored;
- Explore neighbour stack addresses;
Doing so, I find that some addresses after _main_ saved return address in memory are filled with addresses relative to `__libc_start_main` and `__libc_csu_init`. I have my leaks. With these, I can compute relative addresses to ROPgadgets and libc functions, thus pwning the binary.

The exploit works as follows:
- Leak the two address I need for libc and ROP;
- Compute addresses of gadgets and _ret2libc_ through relative offsets, found through gdb on target machine;
- Build the ROPchain:


```POPRSI | 1337 | POPRDI | 1337 | SETREUID | POPRDI | /bin/sh ADDRESS | SYSTEM | EXIT```

- Overwrite saved return address and follow with ROP.


All of this has to be written in Chip-8 instructions. The steps above have been adapted to reflect architectural limits such as number of GP registers :)

Lots of fun to be had with challenges like these. All in all, the attack was quite basic:

1. _Find a leak_
2. _Compute offsets_
3. _Write ROPchain_
4. _Overwrite saved ret address_

But nevertheless, finding and exploiting the vulnerability on such a nerdy architecture proved to be extremely rewarding -- 800 pts :)


You can inspect the final asm code [HERE!](https://github.com/pwnthemole/ctfs/blob/master/icectf2018/twitter/REMOTEPWN.asm)

![AltText1](/media/images/icectftwitter_6.JPG)
