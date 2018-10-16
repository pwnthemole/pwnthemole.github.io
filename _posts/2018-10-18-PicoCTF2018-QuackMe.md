---
title: PicoCTF 2018 - QuackMe WriteUp
layout: post
author: "XxcoralloxX"
tags: reverse PicoCTF2018
category: reverse
---

![AltText](https://i.gyazo.com/176839a2109cb31b08b8e1383cbadc2d.png)

This is an easy reverse challenge.
The program just wants a "password".

Looking with ida we see a "doMagic" function
It reads the password form the user, and store in ebp+PASSWORD
![AltText](https://i.gyazo.com/d60789089c96442f721b71bb55afe405.png)


Here this password is used in a for loop.

![AltText](https://i.gyazo.com/e4da01e2e40def306c142949c5bf37d5.png)

In particular, editing some names to make it more clear, and zooming in the interesting part:

8048858h is a memory address called "sekrutBuffer" containing a string

1 2 3) Put a char form sekrutBuffer[i] into ecx.

4 5 6 7) Put a char from PASSWORD[i] into eax.

8) a xor is performed between sekretBuffer[i] and PASSWORD[i].

9) The resoult is moved into var_1D

10 11 12 13 14) The resoult is compared with greetingMessage[i].

![AltText](https://i.gyazo.com/3dff6af752e54d5bf07ce5f36faf6204.png)

It is quite simple.
So, if Password[i]^sekrutBuffer[i] has to bee equal to greetingMessage[i]
we can get Password reversing the process.
password[i]=sekrutBuffer[i]^greetingMessage[i].

![AltText](https://i.gyazo.com/1b94cef774dfee4bdcf6f1bce4b87cfe.png)

And that's it
picoCTF{qu4ckm3_5f8d9**7}
