---
title: Square CTF 2018 - Gates of hells WriteUp
layout: post
author: "XxcoralloxX"
tags: reverse SquareCTF2018
category: reverse
---

This is a reverse challenge.
As we will see, this is probably a code written directly in assembly, and not some C code compilated.
Since the code is quite short, we will be able to read it all.

First, we try running the binary:

![AltText](https://i.gyazo.com/4918234b46d98a0e21bf0eb77040e3a0.png)

Nothing happens.

Have a look inside:

![AltText](https://i.gyazo.com/6e53f9bd4585f186ec78d2cd279eaab6.png)

We can see that during the first 3 instruction 
a pop takes the number of arguments and compares it with 0x10 (16).

![AltText](https://i.gyazo.com/3288115b512b7441dbaa69caa3ac9332.png)

So we need to provide 15 arguments? (the first is the name of the program).

Ok, 15 arguments, but when will we win?
we can find this function

![AltText](https://i.gyazo.com/93807576fe368fb6a98601cfc369db6f.png)

which is a system call to a print. (which is probably our win function).

as we can see this function will be called if *ebx* will be equal at 0x29A (666)

![AltText](https://i.gyazo.com/2a1b7c5acdbae962b70f390a357e44ab.png)

Otherwise, it will just exit

Ok, we need to understand how to make *ebx* become equal to 0x29A.

Now we follow the code flow after the argument check: 

![AltText](https://i.gyazo.com/5645119bdb54ef348315de0916e6cbbe.png)

A function is called and the value of **ebx which start with 0x25** is stored into the stack and retrieved after the function.
We should investigate this function.

This is the function

![AltText](https://i.gyazo.com/edf556e4ab32ef521317872316209570.png)

Running with gdb we can see that [esi] will contain our input (the 15 arguments provided), and we also notice that every argument is treated as 2 bytes. This means that if our argument is 'A' this function will take 0x41 and 0x0 at the second iteration.
The 3rd iteration will always not respect the jump condition, so will exit.

So, we can reassume that instruction as:
```
	resoult=0;
	bl=0xa;

	for(i=0;i<2;i++){
		ch[i]-=0x30
		if (ch[i]>0x39){
			return resoult;
		}
		resoult=bl*resoult;
		resoult+=dl;
	}
	return resoult;
```
This mean that if we alwaise provide chars >=0x70 we will have

```
resoult=(ch1-0x30)*0xa+(ch2-0x30); 
```

good, that's function is quite predictable then, but what is this for?

Here is the "main" function

![AltText](https://i.gyazo.com/1ceefbb14023df3f1b2f62a95c68b4cd.png)

looking at the entirety of the code we can understand better what it does.

1) The previous function is called, its value will be stored in EAX
2) The result of the function is "stored" in the stack and some strange operations are performed, we will look at that later, after this the value of EAX is retrieved. 
3) If those "strange operation" menage to set the sign flag, *ebx* will be set to 0
4) eax (the result of the function) is used as index of a vector, the content of v[eax] is moved into al (lower part of eax of 1 byte)
5) A mul is performed, so it will exec ```ebx * vet[eax] ```
6) the result is stored into *ebx* again.
7) Here ecx is set at 100. at the instruction n. 10 we can see a loop, so the instruction between point 7 and 10 repeats 100 times.
8) vet2[i] (where 'i' is ecx) is moved into al, and his value will be decreased.
9) if the result will be >= 0 al will be stored back into vet2[i].
10) end of the first loop
11) this an external loop, which loops for 15 times, one for every argument.

So, we want *ebx* to become equal to 0x29A.
it starts with 0x25.
For every cycle ```ebx = ebx * vet[eax]```  (where eax is the return value of our first function).
And, after that, all the value of vet will decrease by 1
Ok, we are close.

Now we want to:

1) Create some code that giving the index needed return to us the argument to provide as input  (reverse the first function)

2) have a better look at the instruction at point 3) which could make *ebx* to reset (and we will lose)

3) Choose the index of the vector, so that their product will be equal to 18 (since *ebx* start to 37 (0x25) 37*18 = 666 (0x29A))


## Task 1
The first task is quite easy.

Since 
```
resoult=(ch1-0x30)*0xa+(ch2-0x30); 
```

we can write a simple code that could find the correct value of ch1 and ch2 giving a result.

![AltText](https://i.gyazo.com/250189b6913b104fc393ae8f20f11c58.png)


## Task 2

Now we want to avoid that *ebx* will be reset.
In order to do that we want eax be such that 
```
aam     12h
aad     0F6h
```
won't provide a negative resoult.

We can find the behavior of those 2 instrctions

https://www.felixcloutier.com/x86/AAM.html
https://www.felixcloutier.com/x86/AAD.html

The first will transform al into a bcd value in base 0x12
the second will do the reverse, but with a different base (0xF6)

Ok, luckily this site also provides a pseudocode, so we could easily write a C function that simulates it.

Here it is:

![AltText](https://i.gyazo.com/fba359793d55b841a18e1a81525b8abe.png)

This will provide all the "bad values" (which are a lot)

Great.

## Task 3

Using gdb we can look at the initial stat of the vecotor:
```
0x80480ca:  0x05	0x09	0x04	0x0f	0x05	0x0b	0x10	0x0e
0x80480d2:	0x0b	0x0d	0x0d	0x08	0x0c    0x07	0x10	0x02
0x80480da:	0x06	0x04	0x0b	0x04	0x02	0x0d	0x07	0x0a
0x80480e2:	0x04	0x0c	0x0e	0x10    0x07	0x06	0x03	0x0e
0x80480ea:	0x01	0x09	0x01	0x0c	0x0e	0x0a	0x0b	0x05
0x80480f2:	0x01	0x09	0x08	0x0d	0x06	0x02	0x10	0x06
0x80480fa:	0x06	0x02	0x03	0x06	0x0b	0x0e	0x05	0x05
0x8048102:	0x03	0x0f	0x01	0x05	0x07	0x0d	0x08	0x05
0x804810a:	0x0c	0x10	0x01	0x02	0x08	0x04	0x0c	0x05
0x8048112:	0x0b	0x0d	0x0d	0x08	0x09	0x03	0x09	0x0a
0x804811a:	0x0c	0x10	0x0b	0x06	0x06	0x0d	0x02	0x0e
0x8048122:	0x0d	0x0e	0x03	0x04	0x01	0x06	0x0c	0x0e
0x804812a:	0x05	0x09	0x01	0x04
```

If we esclude the bad index from provided by the script of the task 2 we get:

```
0x80480ca:  0x05	0x09	0x04	0x0f	0x05	0x0b	0x10	0x0e
0x80480d2:	0x0b	0x0d	0x0d	0x08	0x0c    0x07	0x10	0x02
0x80480da:	0x06	0x04	NULL	NULL	NULL	NULL	NULL	NULL
0x80480e2:	NULL	NULL	NULL	NULL    0x07	0x06	0x03	0x0e
0x80480ea:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x80480f2:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x80480fa:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x8048102:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x804810a:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x8048112:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x804811a:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x8048122:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
0x804812a:	NULL	NULL	NULL	NULL	NULL	NULL	NULL	NULL
```

Now we could wrote a script that chose the right value to make *ebx* equal to 0x29A
But in our case @matpro98 found by hand one solution:

The index where:
34,15,30,17,4,16,28,14,33,5,5,12,9,7,3,6

Now we just want to give those index to the function that transforms them into the input and we find:
0R 15 0N 0A 04 16 0L 14 0Q 05 05 12 09 07 03 06

which is the correct input to make the program print the flag!

Had fun!
