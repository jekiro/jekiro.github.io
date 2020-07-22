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

Beginning research on the binary, by checking the filetype makes it pretty obvious it's a 64 bit ELF executable.  

>chezzz: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2

Running the binary we can see it opens a chess board in the terminal and using the format to move of #L, where # is a number and L is the capital letter to signify the column such as 2B.

![](/content/OEP/chezzz/board.PNG)

So let's look at it in a disassembler, which my choice was IDA although you could use any.  

![](/content/OEP/chezzz/cppmain.PNG)

The main function makes it quite obvious that it's a C++ binary which has quirks that you need to know if you want to fully understand it but that isn't in the scope of this writeup.  

The first function called initializes what is most likely the board in a nested for loop. That can be assumed because the chess board is 8x8 and since arrays always start at 0, the nested for loop is most likely iterating over some sort of structure for the board. Pseudo code for this with some stuff missing for the sake of the writeup would be
```cpp
for(int i = 7; i >= 0; --i) {
    for(int j = 7; j >= 0; --j) {
        init_board_2(r14);
    }
}
```

![](/content/OEP/chezzz/sub_2b5a.PNG)

## Gathering information from Dynamic Analysis

From the information gathered in the previous section, 

## Creating a Z3 script to calculate a correct path

Knowing the path to win, and the mathematical requirements.

### Credits

Credits to my teammate **_kosinw_** for helping with Z3 since I have little experience with it.