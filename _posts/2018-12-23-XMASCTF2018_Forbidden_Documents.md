---
title: X-MAS CTF 2018 - Forbidden Documents
layout: post
author: "madt1m"
category: pwn
tags: pwn file_leak bad_characters got_leak rop_chain
---

Fun things happen in the CTF wild landscape. Like approaching a PWN challenge
with no access to the binary object of the process we are supposed to pwn :)

This has been a fun challenge. Follow my brain while he was trying to
get this flag!

## Binary Exploitation Starter Pack: Getting the Binary

The only thing we can do, for starters, is to interact with the service to find something weird -- or better, of good use.

With a few tries, we quickly understand that the program works like some sort of file retriever:

![Alt](/media/images/xmasforbidden1.JPG)

The first thing I asked myself concerns that "offset" option. Why did they leave me this to _decide_?

(EDIT: No, wait - the first thing I asked myself was "Can i get the flag just asking politely to the service?" and no, I couldn't.)

The answer is quite simple: we cannot retrieve much more than 1200-1300 bytes at once from this binary -- which is something that I did not stop analyzing, since we have that cute offset thing which allows us to retrieve a file chunk after chunk.

Long story short, I used this same service to retrieve the binary file loaded in its heart (kinda meta-phylo-physics, uh?) -- here, briefly, the process:

- Retrieved the file "redir.sh" which I knew, from other challenge, was the name of the shell script dedicated to "instrument" the binary-to-service:

![alt](/media/images/xmasforbidden2.JPG)

Goal! We have a name!
...which gives us a good lead to follow in order to retrieve both the binary **AND** the libc.so object featured in the target machine - which quite always comes handy to fellow pwners :)

> NOTE! </br>
> Retrieving both the object files proved to be not that straightforward. In fact, two main things stole me a certain amount of time:
> - Each \x0a was replaced, in the communication channel, by a \x0a0d;
> - Once the EOF was reached (i.e. the offset + size provided to service was greater than the lenght of the file) we were not noticed. We would've just kept receiving \x00 bytes as data chunks.

What follows is the script I used to retrieve the file, with the given fixes as in before:

[File Retriever](https://gist.github.com/madt1m/c7e6734a228bb4bb903b0f868699297a)

So, with a quick and excited - no, kidding, it took tens of tries - pair of commands:

`python document_retriever.py random_exe_name 1000`

`python document_retriever.py /lib/x86_64-linux-gnu/libc.so.6 1000`

I had finally access to both binary and libc.

## It's Beginning to look a lot like Pwn

All excited and thrilled for the new hunt, we analyze the binary:

![alt](/media/images/xmasforbidden3.JPG)

And look for some easy buffer overflow:

![alt](/media/images/xmasforbidden4.JPG)

Bingo! The `fread()` function delegated to read the file chunk into the stack just happily takes whatever we tell here to fill through the _size_ variable, which is assigned with the "How much should we read" question. This means that, reading a file big enough with a proper _size_ input, we can overflow the saved **EIP** in stack, gaining control of program execution.

`info functions @plt` command in peda confirms us that we have the `puts()` in plt. The 2-stage attack becomes clearer and cleared in our pwning minds:

### FIRST STAGE ROPCHAIN


** POPRDI | PUTS_GOT_PLT | PUTS_PLT | MAIN **

where:
- POPRDI = address of `pop rdi; ret` in the binary. We need this because of the **x86_64 Calling Conventions**.
- PUTS_GOT_PLT = address of the PUTS entry in the GOT. The dynamic linker will load this address with the resolved `puts()` address in libc following the first usage of the function in the program.
- PUTS_PLT = address of the PLT stub code for the `puts()` function.
- MAIN = the `main()` function address. We need this in order to re-run the main function and send the second stage, with the info leaked from GOT, and the libc derandomized.

If something in this process doesn't seem clear here, I'd suggest you to ask a search engine about [Leaking GOT](http://lmgtfy.com/?q=Exploit+Development+Leaking+GOT) :)

### SECOND STAGE ROPCHAIN

** POPRDI | BIN_SH_ADDRESS | SYSTEM_ADDRESS **

Where obviously, `"/bin/sh"` and `system()` addresses in libc are de-randomized using leak.

Ok then, everything works here, but...how can we control the content of the buffer to be overflown?

The hint to solve this came straight from the binary, precisely:

![alt](/media/images/xmasforbidden5.JPG)

The check for _flag_ is obvious, but...what about STDIN?

Yes, you got it right.
Opening stdin basically means that the `fread()` function would write our arbitrary input to the buffer, so that we can realize our best dreams of _pwn4g3_.

> "There are other ways to do this too"

As in before, the hint comes from the binary itself. In Linux, there are quite a few ways to access I/O as files.

After some study, we came out with `"/proc/self/fd/0"` as a valid alias for STDIN, which worked. I had full access to the buffer :)

A bit of context now:

>I had to go out for a dinner. I was sitting in front of my laptop, the clock showed 8:00 PM. I still had 30 minutes to get ready and prepare for the night, and I managed to successfully pwn the exploit locally. Finally relieved, I change offsets and address in the exploit, and launch it. Nothing. EOF.

The reason behind this brief, little, sad story takes a name sadly famous: _Bad characters_.

It seems that the connection on the remote side is dropping some bytes in the fopen, including the `\x12`, and the thing is, the `main` address of the first stage happens to contain one of those bytes.

But we do not lose hope and courage: there's a return address to main stored in stack, just one word after the location where we stored the main address :)

Therefore, we slightly modify the 1st stage ROP chain to:

** POPRDI | PUTS_GOT_PLT | PUTS_PLT | RET **

The exploit, complete:

[Exploit](https://gist.github.com/madt1m/e80f73ad052f0f7be91f714547720ced)

X-MAS{r34d1n6_f0rb1dd3n_b00k5_15_50_much_fun}
