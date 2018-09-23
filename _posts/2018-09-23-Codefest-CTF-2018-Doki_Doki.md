---
title:  Codefest CTF 2018 - Doki Doki
layout: post
author: "XxcoralloxX"
tags: reverse CodefestCTF2018
---

It was a simple reverse engineering challenge.

We need to provide 3 Keys in order to get the flag.

My first try was to avoid every "game over" skipping via gdb all the check functions, but the flag provided at the end wasn't correct, so it needs to be looked more carefully with IDA (or any disassembler).

## Nice to meet you Monika
Monika, the main character of the story asks the first key.
On the right, we can see a loop until the user inserts the string, on the left the call at the function "checkPoem" 
![AltText](https://i.gyazo.com/1cd52d7a2215be80e94025251d59511f.png)



-----


### Check 1
Let's have a look,
It's easy to see that there is a string in the variable "aMyHeadIsAHiveF" moved from memory and a strcmp.
checking that variable we found "My head is a hive full of words that won't settle", the first key.
After the check we see also some character moved into a variable "flg", basically, after every check, some chars are added into the flag.

![AltText](https://i.gyazo.com/11148cb9f185e509000f4f190e768868.png)


-----

### Check 2
The second check is made by the function "checkHiddenMeaning"
Here we see that this is a wrapper. the check function is: "findHidden", 
but we can also see a for loop which edit some chars of the flag, and after that, 3 more chars are edited.
The good news is that the key isn't used at all, so we can just patch the program in order to make writing the flag even if the key is wrong. 
btw findHidden is like a checksum of the key, no need to waste time on it since it doesn't touch the flag.

![AltText](https://i.gyazo.com/24c522a2a77eb80733d1e2513e9a97d4.png)


-----

### Check 3
Last check key is "posterTitle".
A first loop, edit the first 4 chars of the key.

![AltText](https://i.gyazo.com/a83c861308044403974839c4869146ee.png)




Then we have another loop which calls 4 thread running the "checkTitle" function.

![AltText](https://i.gyazo.com/813af48bb8859e34cc8ea23859360444.png)


-----


checkTitle was quite hard to follow, a vector of functions was called, but hard to say what those functions do.
But there's also a doSomething function, more readable

As we can see here a fixed seed is given to the srandom function, then in the for, rand() is called, the number is manipulated, and at the end, a mov put a char into the flag.
We also see a string conteining several characters inside, so probably what happen is 
```
srandom(seed);
for(i=6;i<12;i++){
	 falg[i]=string[rand()]
	}
```

![AltText](https://i.gyazo.com/38d7ef6cdaed8d5f1b9629d80d7a00aa.png)


-----



Maybe this means that even in this case the flag does not depend from the key?
(Spoiler, yes.. luckily)
Let's go back to the checkTitle and delete all the call to function except for the doSomething, otherwise, they cause the program to stop if the key isn't correct.

Good. The last problem was the function "wrapUp" which call the "endlessTalk" if the Access function doesn't return the right value, I just patched the jump to avoid the problem.

![AltText](https://i.gyazo.com/83a341882f32a36087833da4c4160fd4.png)

And here we are, just apply all the edits and run the program to get the correct flag.




-----



XxcoralloxX
