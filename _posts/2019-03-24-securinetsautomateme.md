---
title: SecurinetsCTF 2019  - Automate Me Writeup
layout: post
author: "mr96"
category: reverse
tags: reverse python
---
# Automate Me (919 pts., 65 solves)
We're given a binary. Trying to open it in GDB we find that there is a lot of code in the main, so it is almost impossible to read it all by hand. Scrolling the first part we find a recurrent schema: the binary tries to verify a key character by character, and there are basically 2 types of comparisons.

The first one is a plain comparison, like the following one

```
.text:0000000000003A8E loc_3A8E:                               ; CODE XREF: main+339C↑j
.text:0000000000003A8E                 mov     rax, [rbp+var_20]
.text:0000000000003A92                 add     rax, 8
.text:0000000000003A96                 mov     rax, [rax]
.text:0000000000003A99                 add     rax, 111h
.text:0000000000003A9F                 movzx   eax, byte ptr [rax]
.text:0000000000003AA2                 cmp     al, 61h ; 'a'
.text:0000000000003AA4                 jz      short loc_3ABC
.text:0000000000003AA6                 lea     rdi, aNope      ; "nope :( "
.text:0000000000003AAD                 mov     eax, 0
.text:0000000000003AB2                 call    _printf
.text:0000000000003AB7                 jmp     locret_283A0
```

The second one is a xored comparison, like this one:
```
.text:0000000000003ABC loc_3ABC:                               ; CODE XREF: main+33CA↑j
.text:0000000000003ABC                 mov     rax, [rbp+var_20]
.text:0000000000003AC0                 add     rax, 8
.text:0000000000003AC4                 mov     rax, [rax]
.text:0000000000003AC7                 movzx   eax, byte ptr [rax+112h]
.text:0000000000003ACE                 mov     [rbp+var_1], al
.text:0000000000003AD1                 xor     [rbp+var_1], 0EBh
.text:0000000000003AD5                 cmp     [rbp+var_1], 85h
.text:0000000000003AD9                 jz      short loc_3AF1
.text:0000000000003ADB                 lea     rdi, aNope      ; "nope :( "
.text:0000000000003AE2                 mov     eax, 0
.text:0000000000003AE7                 call    _printf
.text:0000000000003AEC                 jmp     locret_283A0
```

So basically I used `objdump -d bin > out.txt` and parsed the output of the xored ones with python as follows

```
lines = [line.rstrip('\n').replace('\t','') for line in open('out.txt')]

c = []
key = 0xeb

for l in range(len(lines)):
    if "$0xeb" in lines[l]:
        c.append(lines[l])
        c.append(lines[l+1])

c2 = []
for l in c:
    if "$0xeb" not in l:
        c2.append(l)
for l in c2:
    #print(l.split(",")[0][-2:])
    n = int(l.split(",")[0][-2:],16)
    print(chr(n^key), end="")
```

Having this output i simply reconstructed the flag by hand using the parts in clear (in about 10 minutes).
`securinets{automating_everything_is_the_new_future}`
