---
title: hacklu - Baby Reverse WriteUp
layout: post
author: "XxcoralloxX"
tags: reverse hacklu
category: reverse
---

This is a simple reverse challenge.

![AltText](https://i.gyazo.com/47f9e6289af1741527a53e4ac3cc80b1.png)

With ida we can see inside the assembly.
![AltText](https://i.gyazo.com/966e6b0fefff4f59f486a1f1667d41da.png)

A call to 400082 is performed as soon as the program start.

Looking at this function we can see what's happening:

![AltText](https://i.gyazo.com/f599f6f05728ce8444311eb206e57f79.png)

As you can see, 2 syscalls are performed, one to print the message and one to read the key.
Then, there's a for loop where is happening some manipulation like

```
key[i]=key[i]^key[i+1]
```

after that manipulation, we can see that a 'repe cmpsb' is performed.

```
Note: repe repeat the next code (cmp in this case) as many times as the value of ecx.
```

Debugging with gdb, we can see more cleary what is happening.
We notice that this instruction does a cmp between the flag and a fixed string, one byte at the time
![AltText](https://i.gyazo.com/07c45b50a023c3c4ac2e7eafe98a053c.png)


let's see inside this string we find:

```
0x0a, 0x0d, 0x06, 0x1c, 0x22, 0x38, 0x18, 0x26, 0x36, 0x0f, 0x39, 0x2b, 0x1c, 0x59, 0x42, 0x2c, 0x36, 0x1a, 0x2c, 0x26, 0x1c, 0x17, 0x2d, 0x39, 0x57, 0x43, 0x01, 0x07, 0x2b, 0x38, 0x09, 0x07, 0x1a, 0x01, 0x17, 0x13, 0x13, 0x17, 0x2d, 0x39, 0x0a, 0x0d, 0x06, 0x46, 0x5c, 0x7d
```

Now it's time to script, to generate the key.
We don't know the initial char of the key, but we know this property:
key[i]=key[i]^key[i+1]
So we can script to generate all possible key:

![AltText](https://i.gyazo.com/8d4c191b4acd156cb2b27de3173d1982.png)

and this is what we can find in the output

![AltText](https://i.gyazo.com/2f9acab31f749f1bb262fa6a4d34b73b.png)

XxcoralloxX
