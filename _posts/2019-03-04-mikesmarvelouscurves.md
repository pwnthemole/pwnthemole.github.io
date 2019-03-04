---
title: TAMUctf - Mike's Marvelous Mistery Curves Writeup
layout: post
author: "matpro98"
category: crypto
tags: crypto ecc
---

## Challenge description
Mike, the System Administrator, thought it would be a good idea to implement his own Elliptic Curve Diffie Hellman key exchange using unnamed curves to use across the network. We managed to capture network traffic of the key exchange along with an encrypted file transfer. See if you can read the contents of that file.

Note: The password to the AES192-CBC encrypted file is the shared key x and y coordinates from the key exchange concatenated together. (e.g. sharedKey = (12345,67890) password = "1234567890")

Difficulty: hard

Edit: 02/23/2019 14:33 Changed AES256-CBC to AES192-CBC

## Solution

The file we have is `key_exchange.pcap`. Here we can find three streams: the two certificates and the encrypted file. For example, one of the certificates is the following:

```
-----BEGIN CERTIFICATE-----
Q2VydGlmaWNhdGU6CiAgICBEYXRhOgogICAgICAgIFZlcnNpb246IDMgKDB4MikKICAgICAgICBTZXJpYWwgTnVtYmVyOgogICAgICAgICAgICBiOTo1OTpkYTpjNDpkNzozZjpiYzozMQogICAgU2lnbmF0dXJlIEFsZ29yaXRobTogYmFzZTY0CiAgICAgICAgSXNzdWVyOiBDID0gVVMsIFNUID0gVGV4YXMsIEwgPSBDb2xsZWdlIFN0YXRpb24sIE8gPSBUZXhhcyBBJk0gVW5pdmVyc2l0eSwgT1UgPSB0YW11Q1RGLCBDTiA9IEFsaWNlLCBlbWFpbEFkZHJlc3MgPSBhbGljZUB0YW11Y3RmLmVkdQogICAgICAgIFZhbGlkaXR5CiAgICAgICAgICAgIE5vdCBCZWZvcmU6IE9jdCAgOSAxMzowODoxMiAyMDE4IEdNVAogICAgICAgICAgICBOb3QgQWZ0ZXIgOiBOb3YgIDggMTM6MDg6MTIgMjAxOCBHTVQKICAgICAgICBTdWJqZWN0OiBDID0gVVMsIFNUID0gVGV4YXMsIEwgPSBDb2xsZWdlIFN0YXRpb24sIE8gPSBUZXhhcyBBJk0gVW5pdmVyc2l0eSwgT1UgPSB0YW11Q1RGLCBDTiA9IEFsaWNlLCBlbWFpbEFkZHJlc3MgPSBhbGljZUB0YW11Y3RmLmVkdQogICAgICAgIFN1YmplY3QgUHVibGljIEtleSBJbmZvOgogICAgICAgICAgICBQdWJsaWMgS2V5IEFsZ29yaXRobTogaWQtZWNQdWJsaWNLZXkKICAgICAgICAgICAgICAgIFB1YmxpYy1LZXk6CiAgICAgICAgICAgICAgICAgICAgNjE4MDEyOTI2NDcKICAgICAgICAgICAgICAgICAgICAyMjgyODgzODUwMDQKICAgICAgICAgICAgICAgIEFTTjEgT0lEOiBiYWRQcmltZTk2djQKICAgICAgICAgICAgICAgIENVUlZFOiBKdXN0Tm8KICAgICAgICAgICAgICAgICAgICBGaWVsZCBUeXBlOiBwcmltZS1maWVsZAogICAgICAgICAgICAgICAgICAgIFByaW1lOgogICAgICAgICAgICAgICAgICAgICAgICA0MTIyMjAxODQ3OTcKICAgICAgICAgICAgICAgICAgICBBOiAgIAogICAgICAgICAgICAgICAgICAgICAgICAxMDcxNzIzMDY2MTM4MjE2MjM2MjA5ODQyNDQxNzAxNDcyMjIzMTgxMwogICAgICAgICAgICAgICAgICAgIEI6ICAgCiAgICAgICAgICAgICAgICAgICAgICAgIDIyMDQzNTgxMjUzOTE4OTU5MTc2MTg0NzAyMzk5NDgwMTg2MzEyCiAgICAgICAgICAgICAgICAgICAgR2VuZXJhdG9yOgogICAgICAgICAgICAgICAgICAgICAgICA1Njc5Nzc5ODI3MgogICAgICAgICAgICAgICAgICAgICAgICAzNDkwMTg3Nzg2MzcKICAgICAgICBYNTA5djMgZXh0ZW5zaW9uczoKICAgICAgICAgICAgWDUwOXYzIFN1YmplY3QgS2V5IElkZW50aWZpZXI6IAogICAgICAgICAgICAgICAgRjA6NEU6QkY6ODc6OTI6MTY6OUI6RDY6NTM6REE6Q0M6NkQ6QUI6MjI6MEU6NDA6MjU6NDE6QzU6Q0MKICAgICAgICAgICAgWDUwOXYzIEF1dGhvcml0eSBLZXkgSWRlbnRpZmllcjogCiAgICAgICAgICAgICAgICBrZXlpZDpGMDo0RTpCRjo4Nzo5MjoxNjo5QjpENjo1MzpEQTpDQzo2RDpBQjoyMjowRTo0MDoyNTo0MTpDNTpDQwoKICAgICAgICAgICAgWDUwOXYzIEJhc2ljIENvbnN0cmFpbnRzOiBjcml0aWNhbAogICAgICAgICAgICAgICAgQ0E6VFJVRQogICAgU2lnbmF0dXJlIEFsZ29yaXRobTogZWNkc2Etd2l0aC1TSEEyNTYKICAgICAgICAgMzA6NDY6MDI6MjE6MDA6Y2M6M2M6ODQ6ZWI6MTk6NzM6ZTE6NjI6N2Y6ODE6Nzg6OTk6YzY6CiAgICAgICAgIDI2OmI4Ojg2OjllOjYxOjdlOjgyOjg3OmYxOjg1OjVjOjc1OmUxOjJkOjYwOjM3OjU1OmI2OgogICAgICAgICAwOTowMjoyMTowMDo4NTozMzphZjpkYzozNDowZjplNToxMzo4ZToyNjo4ODowNjphMzoxMzoKICAgICAgICAgZDE6YTI6ZWQ6ZDU6MDQ6Y2I6OWM6NTA6ZDE6YzQ6YTQ6NGQ6NDI6OTI6YmQ6Njk6NTY6MWEK
-----END CERTIFICATE-----
```

which, decoded as base64, is:

```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            b9:59:da:c4:d7:3f:bc:31
    Signature Algorithm: base64
        Issuer: C = US, ST = Texas, L = College Station, O = Texas A&M University, OU = tamuCTF, CN = Alice, emailAddress = alice@tamuctf.edu
        Validity
            Not Before: Oct  9 13:08:12 2018 GMT
            Not After : Nov  8 13:08:12 2018 GMT
        Subject: C = US, ST = Texas, L = College Station, O = Texas A&M University, OU = tamuCTF, CN = Alice, emailAddress = alice@tamuctf.edu
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key:
                    61801292647
                    228288385004
                ASN1 OID: badPrime96v4
                CURVE: JustNo
                    Field Type: prime-field
                    Prime:
                        412220184797
                    A:   
                        10717230661382162362098424417014722231813
                    B:   
                        22043581253918959176184702399480186312
                    Generator:
                        56797798272
                        349018778637
        X509v3 extensions:
            X509v3 Subject Key Identifier:
                F0:4E:BF:87:92:16:9B:D6:53:DA:CC:6D:AB:22:0E:40:25:41:C5:CC
            X509v3 Authority Key Identifier:
                keyid:F0:4E:BF:87:92:16:9B:D6:53:DA:CC:6D:AB:22:0E:40:25:41:C5:CC

            X509v3 Basic Constraints: critical
                CA:TRUE
    Signature Algorithm: ecdsa-with-SHA256
         30:46:02:21:00:cc:3c:84:eb:19:73:e1:62:7f:81:78:99:c6:
         26:b8:86:9e:61:7e:82:87:f1:85:5c:75:e1:2d:60:37:55:b6:
         09:02:21:00:85:33:af:dc:34:0f:e5:13:8e:26:88:06:a3:13:
         d1:a2:ed:d5:04:cb:9c:50:d1:c4:a4:4d:42:92:bd:69:56:1a
```

So we have the elliptic curve's parameters:

```
p = 412220184797
A = 10717230661382162362098424417014722231813
B = 22043581253918959176184702399480186312
P = (56797798272, 349018778637)
```

Alice's public key:

```
Q_a = (61801292647, 228288385004)
```

Bob's public key:

```
Q_b = (196393473219, 35161195210)
```

So, I tried to break these keys using Baby step - Giant step algorithm, and it worked! Here is the code:

```
p = 412220184797
A = 10717230661382162362098424417014722231813
B = 22043581253918959176184702399480186312
(xP, yP) = (56797798272, 349018778637)
(xQ_a, yQ_a) = (61801292647, 228288385004)
(xQ_b, yQ_b) = (196393473219, 35161195210)
P = [xP, yP]
Q_a = [xQ_a, yQ_a]
Q_b = [xQ_b, yQ_b]
F = FiniteField (p)
E = EllipticCurve (F , [A ,B])
P = E.point(P)
Q_a = E.point(Q_a)
Q_b = E.point(Q_b)
n = E.order()
m = ceil(sqrt(n))
R = P
precomputed = {P : 1}
for a in range(2, m):
    R = R + P
    precomputed[R] = a
R = Q_a
S = (-m) * P
found=False
for b in range(m):
    try:
        a = precomputed[R]
    except KeyError:
        pass
    else:
        k_a = a + m * b
        found = True
        print(k_a)
        print(k_a * P == Q_a)
        break
    R = R + S
R = Q_b
S = (-m) * P
found=False
for b in range(m):
    try:
        a = precomputed[R]
    except KeyError:
        pass
    else:
        k_b = a + m * b
        found = True
        print(k_b)
        print(k_b * P == Q_b)
        break
    R = R + S
if not found:
    print("Log not found")
else:
    S=k_a * k_b * P
    print(S)
```

and the output is:

```
54628069049
True
6895697291
True
(130222573707 : 242246159397 : 1)
```

so the AES key is `130222573707242246159397`.

Now, the hardest part (for me) was to extract the AES-encrypted file from the pcap file. After several attempts, I managed to have my copy of that file. With the following script I decrypted the file:

```
import os, random, struct
from Crypto.Cipher import AES

key = '130222573707242246159397'
IV = 16 * '\x00'
mode = AES.MODE_CBC

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, 'rb') as infile:
        iv = IV
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                dec=decryptor.decrypt(chunk)
                outfile.write(dec)
                print(dec)

decrypt_file(key,"encrypted","out.txt",16)
```

In `out.txt` there was a passage from `The Hitchhiker's Guide to the Galaxy` with the flag `gigem{Forty-two_said_Deep_Thought}`.
