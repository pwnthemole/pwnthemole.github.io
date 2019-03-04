---
title: OtterCTF - PDFuck Writeup
layout: post
author: "matpro98"
category: misc
tags: misc PDF
---

## Challenge description
I found some intresting PDF and file on my otter PC. take a look and see if you can get the secret message.

## Solution
We have a PDF named `history.pdf`, let's have a look inside! The title of the file is `The Philosophy of History` from `Georg Wilhelm Friedrich Hegel`. Ugh, maybe the philosopher I like the least. But it seems simply his book. So let's try with the other file, `PCFuck.txt`.

This time we have a file with more or less $$600$$ couples of integers. While the second number of each couple can be quite large, the first one seems smaller and a rapid check confirmed me that the max value of the first elements is less than the number of the pages in Hegel's book. So I wrote a simple Python script that extracts the letters pointed by the couples (interpreted as $$(page,letter)$$) in the txt file. Here is the script:

```
import PyPDF2

with open("PDFuck.txt") as f:
    content = f.readlines()
content = [x.strip().split(' ') for x in content]

file = open('history.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)

if fileReader.isEncrypted:
    fileReader.decrypt('')

first=[]
second=[]
for i in content:
    first.append(int(i[0][:-1]))
    second.append(int(i[1]))

res=""
for i in range(len(first)):
    page = fileReader.getPage(first[i])
    page_content = page.extractText()
    res = res + page_content[second[i]]
print(res)
```

and here is the output:

```
Q29uZ3JhdHVsYXRpb25zISBpZiB5b3UgbWFkZSBpdCB0aGF0IGZhciB0aGF0IG1lYW5zIGVpdGhlciB5b3UgYXJlIG9uZSBtb3RpdmF0ZWQgYmFzdGVyZWQsIG9yIHlvdSBrbm93IHB5dGhvbiAtXy0uLi4gQW55d2F5Li4uIGZvbGxvdyB0aGlzIGxpbmsgOiBodHRwczovL3d3dy55b3V0dWJlLmNvbS93YXRjaD92PWY3c3h3SExSS0tnDQpoaW50OiAuLi0uIC4tLi4gLi0gLS0uIC8gLi0tLiAuLS4uIC4uLSAuLi4gLyAuLS0tLSAtLS0uLi4gLS0tLS0gLS0tLi4gLS4uLi4tIC4tLS0tIC0tLS4uLiAuLS0tLSAtLS0uLiAvIC4tLi4gLS0tIC4tLSAuIC4tLiAtLi0uIC4tIC4uLiAuIC8gLi0tIC4uIC0gLi4uLiAvIC4uLSAtLiAtLi4gLiAuLS4gLi4uIC0uLS4gLS0tIC4tLiAuIC8gLi0gLi4uIC8gLi4uIC4tLS4gLi0gLS4tLiAuIC4uLiAvIC4tLSAuLS4gLi0gLi0tLiAuLS0uIC4gLS4uIC8gLi0tIC4uIC0gLi4uLiAvIC0uLS4gLi4tIC4tLiAuLS4uIC0uLS0gLyAtLi4uIC4tLiAuLSAtLi0uIC0uLSAuIC0gLi4u
```

Decoding it from base64, we get:

```
Congratulations! if you made it that far that means either you are one motivated bastered, or you know python -_-... Anyway... follow this link : https://www.youtube.com/watch?v=f7sxwHLRKKg
hint: ..-. .-.. .- --. / .--. .-.. ..- ... / .---- ---... ----- ---.. -....- .---- ---... .---- ---.. / .-.. --- .-- . .-. -.-. .- ... . / .-- .. - .... / ..- -. -.. . .-. ... -.-. --- .-. . / .- ... / ... .--. .- -.-. . ... / .-- .-. .- .--. .--. . -.. / .-- .. - .... / -.-. ..- .-. .-.. -.-- / -... .-. .- -.-. -.- . - ...
```

The link redirect us to a YouTube video, `The Otter Song`, but the hint revealed me ho to get the flag. In fact, it is encrypted in the Morse alphabet and the plaintext is:

```
FLAG PLUS 1:08-1:18 LOWERCASE WITH UNDERSCORE AS SPACES WRAPPED WITH CURLY BRACKETS
```

and the flag is `flag{i_swam_with_the_otter_and_we_played_in_the_pool}`.
