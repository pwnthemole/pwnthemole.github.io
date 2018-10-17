---
title: PicoCTF 2018 - Radix's Terminal WriteUp
layout: post
author: "XxcoralloxX"
tags: reverse PicoCTF2018
category: reverse
---


Here we have another reverse challenge:

![AltText](https://i.gyazo.com/ab17f08ce0d886c624c7cfa242195f52.png)

Let's see inside this:

This part is simple, there are 3 branches, one for the "missing password", one for the "wrong password" and the last for "correct password".

![AltText](https://i.gyazo.com/df975a2c9d131b8235557366f4a489d2.png)

Notice when we take this last branch seems that the flag isn't actually printed, but only a message with "So where is my flag?"
That's probably mean that the flag is the password itself.

### check password

This function isn't really easy to reverse, but let's have a look slowly:

in the first block we notice that the password is measured with a strlen:

![AltText](https://i.gyazo.com/b7b23f1131fea175dcc0d72829100c35.png)

Next, we have a bifurcation which is basically a for loop on the password length.

Isn't easy to follow, but here we can see that 3 chars of the password are taken:
![AltText](https://i.gyazo.com/b5e3af3b56a7c323b54a7f58e6d104b6.png)
![AltText](https://i.gyazo.com/0e8ec4cc908641730815d01d32692e3d.png)


Whit those 3 chars (var14 is the last char taken from the password ) some operations are performed:

Focus first on the yellow part

![AltText](https://i.gyazo.com/88360dac833890e6b87ad360503a38b1.png)

What it does is:

```
resoult(ebp+var_10) = (char2 << 8) + (char1 << 16) + char3;
```

Next, we have some similar code repeated x4 times with only a small change on the shift (shr instructions):

![AltText](https://i.gyazo.com/13cdf84616031dc2320589be4a67e114.png)

Seems that it is doing:

```
pass[j++] = alph[(resoult >> 18) & 0x3F];
pass[j++] = alph[(resoult >> 12) & 0x3F];
pass[j++] = alph[(resoult >> 6) & 0x3F];
pass[j++] = alph[resoult & 0x3F];
```

alphabet is just a string of some chars (67):

![AltText](https://i.gyazo.com/8838d3e9e7f70ab60f949862b4916c4f.png)

## we are close

after this for we see a strcmp:

![AltText](https://i.gyazo.com/7df4eb3d532c857e96a596eb198ed8c5.png)

so here what's happening here:
for every 3 chars of the password, 4 chars of a new string are generated.
This new string is compared to a fixed one, and if are equal we get a win.

## The vulnerability?

The vulnerability here is that even if it is a 14 chars long password, we can "check" if it is right splitting it into groups of 4 since every group isn't "correlated" whit the next.

That's mean that a brute force has to check only (67^4)x4 possible combinations instead of 67^14.

We now put down some code to do this:

![AltText](https://i.gyazo.com/3dbda86326de3f6176707f373471c8df.png)

and here is the flag:

picoCTF{bAsE_64_eNCoDiNg_iS_EAsY_195***83}

Whait.. what? base64... oh.. well nevermind...

XxcoralloxX
