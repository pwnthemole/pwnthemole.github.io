---
title: PicoCTF 2018 - QuackMe-Up WriteUp
layout: post
author: "XxcoralloxX"
tags: reverse PicoCTF2018
category: reverse
---

Here is a new reverse challenge.

![AltText](https://i.gyazo.com/b66afcc3a6074654aa9b36a536d24199.png)

It is really intuitive, just running the programme we see that it "encrypt" your password, and print it.
We need to dequack: "11 80 20 E0 22 53 72 A1 01 41 55 20 A0 C0 25 E3 20 30 00 45 05 35 40 65 C1"

The encryption seems to be done char by char and since same chars are encrypted in the same way we just need to "map" the output value of every char. (Black box analysis)

So:

I obtain all the encrypted chars (forgot '_')

![AltText](https://i.gyazo.com/3576dbbbbf556e5f8ebeaacaf745ac92.png)

And wrote a script that decrypt every char:

![AltText](https://i.gyazo.com/4d3b1862345b3a987e9e0fa5d8b18b88.png)

And that's it, really simple:
picoCTF{qu4ckm3_cba51**7}
