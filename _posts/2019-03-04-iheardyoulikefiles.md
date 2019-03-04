---
title: TAMUctf - Iheard you like files Writeup
layout: post
author: "matpro98"
category: misc
tags: misc PDF
---

## Challenge description
Bender B. Rodriguez was caught with a flash drive with only a single file on it. We think it may contain valuable information. His area of research is PDF files, so it's strange that this file is a PNG.

Difficulty: easy-medium

## Solution
The challenge give us an image called `art.png`. Since we are looking for a PDF file, with the command `binwalk -D pdf art.png` we can find a PDF file. Great! Wait, no... there we can find this sentence: `Wait...is this a pdf?
I guess if it looks like a duck, and quacks like a duck, it could still be a pigeon.` so I starded thinking that we can't find the flag this way. Lets go back!

Then we can try extracting everything we can: `binwalk -e art.png` returns a lot of stuff. In particular we have another image in `word/media`. Let's try `binwalk -D pdf image1.png`, maybe this time we're luckier. In we can spot the PDF file named `1485`. The output of `strings 1485` ends with a suspicious line: `ZmxhZ3tQMGxZdEByX0QwX3kwdV9HM3RfSXRfTjB3P30K`, which is `flag{P0lYt@r_D0_y0u_G3t_It_N0w?}` encoded in base64. So now we have solved the challenge!
