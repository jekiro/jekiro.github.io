---
layout: single
title: "redpwn-2020 chezzz writeup"
header:
  teaser: /assets/images/teasers/mango.png
excerpt: "Chezzzboard was a reversing challenge in the redpwn 2020 CTF that involved z3 to solve math problems."
---

### Challenge Information

Challenge: chezzzboard  
Created by: dns  
Files: [chezzz (not uploaded yet)](/assets/files/chezzz)
>I'll also give you the flag if you beat me in chess  
>nc 2020.redpwnc.tf 31611

## Basic Research and Static Analysis

```go
var test = "TESTING"
test3 := 2
```

Beginning research on the binary, by checking the filetype makes it pretty obvious it's a 64 bit ELF executable.  

>chezzz: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=25c612f70c8b72ad9cfd93ef62542c08c94f47e0, for GNU/Linux 3.2.0, stripped

Running the binary we can see it opens a chess board in the terminal and using the format to move of #L, where # is a number and L is the capital letter to signify the column.

![](/content/oep/chezzz/board.png)



## Gathering information from Dynamic Analysis

From the information gathered in the previous section, 

## Creating a Z3 script to calculate a correct path

Knowing the path to win, and the mathematical requirements.

### Credits

Credits to my teammate **_kosinw_** for helping with Z3 since I have little experience with it.