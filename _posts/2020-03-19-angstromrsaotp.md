---
title:  ångstromCTF 2020 - RSA-OTP Writeup
layout: post
author: "matpro98"
category: crypto
tags: crypto oracle
---
For this challenge we are provided with the server source:
```
from Crypto.Util.number import bytes_to_long
from Crypto.Random.random import getrandbits # cryptographically secure random get pranked
from Crypto.PublicKey import RSA
from secret import d, flag
# 1024-bit rsa is unbreakable good luck
n = 136018504103450744973226909842302068548152091075992057924542109508619184755376768234431340139221594830546350990111376831021784447802637892581966979028826938086172778174904402131356050027973054268478615792292786398076726225353285978936466029682788745325588134172850614459269636474769858467022326624710771957129
e = 0x10001
key = RSA.construct((n,e,d))

f = bytes_to_long(bytes(flag,'utf-8'))
print("Encrypted flag:")
print(key.encrypt(f,0)[0])

def otp(m):
	# perfect secrecy ahahahaha
	out = ""
	for i in bin(m)[2:]:
		out+=str(int(i)^getrandbits(1))
	return out

while 1:
	try:
		i = int(input("Enter message to sign: "))
		assert(0 < i < n)
		print("signed message (encrypted with unbreakable otp):")
		print(otp(key.decrypt(i)))
	except:
		print("bad input, exiting")
		break
```

At the beginning I was a little bit confused by the comments: usually when something is pointed to as secure, it is what you have to break; unfortunately not this time. So I spent some hours trying to factorize $$n$$ and to attack directly the `otp` function.
Then I tried to modify one of our attempt to break `otp`: in fact it is an oracle and in particular it leaks the lenght of the decrypted message.
The first thing to notice is that if we send to the server $$c$$ and $$c\cdot 2^{-e} \pmod{n}$$, then (calling $$m$$ the decrypted $$c$$):
* if $$m$$ is even, then the second response is exactly one bit shorter then the first one
* if $$m$$ is odd, the lengths of the first and second response are uncorrelated

Don't worry, we can still recover our flag: in fact $$n$$ is odd, thus if we could operate on the decrypted $$m$$ we ccould also change it from odd to even by adding $$n$$. But what happens?
We are working modulo $$n$$, so we have $$m<n;\ m+n<2n;\ \dfrac{m+n}{2}<n$$ and $$\dfrac{m+n}{2}\equiv \dfrac{m}{2} \pmod{n}$$. This means that if at some point $$m$$ is even, then sending $$c\cdot 2^{-e} \pmod{n}$$ we know the length of $$\dfrac{m}{2}$$, otherwise we know the length of $$\dfrac{m+n}{2}$$.

We can extend the reasoning to more than one bit. Let's construct $r$ in this way:
* send to the server the encrypted flag (let's call it $$c$$) and call $$l_0$$ the bit length of the response
* send to the server $$c\cdot 2^{-e} \pmod{n}$$ and call $$l_1$$ the bit length of the response
* if $$l_1$$ is equal to $$l_0-1$$, then prepend a 0 to $$r$$, otherwise a $$1$$ (we are interpreting $$r$$ in binary)
* repeat these steps enough (we need $$l_0$$ bits)

We can now notice that after $$i$$ steps we know the parity of $$\dfrac{rn+f}{2^i}$$ (let's call it $$p$$), so we can recover the last $$i$$ bits of $$f$$ as $$p2^i-rn \pmod{2^{i+1}}$$.
That's all: we can recover all the bits of $$f$$, leading us to the flag `actf{this_is_not_what_i_meant_when_i_told_you_to_use_rsa_with_padding}`.
