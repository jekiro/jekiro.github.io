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

After main initializes the board with the function above, it ends up calling the function shown below which has an initialization function with another nested for loop at **sub_12B8** so 
we can ignore 12B8 somewhat, and also calls a bigger function that is at 159A. As you may also notice rax gets moved into rdi for every function called and in the main function it points to an allocated structure on the stack of size 0x408 or so. That will be useful knowledge to come to understand how the binary works. 

![](/content/OEP/chezzz/sub_1b8a.PNG)

Looking at **sub_159A** it is pretty obvious that it is doing most of the handling for the chess board just from the size. 

![](/content/OEP/chezzz/sub_159a_graph.PNG)

While a function that is big and has calls to other functions might seem daunting, looking through it slowly one of the very first things that caught my eye was the call to **system**.

![](/content/OEP/chezzz/sub_159a_system.PNG)

Tracing the system calls backwards shows it depends on the returning value from **sub_2792** equaling **467** so rename 2792 to **f_checkwin** to make it more understandable.

![](/content/OEP/chezzz/sub_159a_2792.PNG)

The win check function has a jump table that leads to different code blocks depending on the return of the function **sub_1272**.  
This isn't being detected by IDA so you can create a manual definition for a switch idiom by clicking where it starts which is the ja instruction for this example and setting the values correctly.

![](/content/OEP/chezzz/win_ex.PNG)

![](/content/OEP/chezzz/win_switch.PNG)

## Filling missing knowledge with Dynamic Analysis

From the information gathered in the previous section, 

## Creating a Z3 script to calculate a correct path

Knowing the path to win, and the mathematical requirements.

### Credits

Credits to my teammate **_kosinw_** for helping with Z3 since I have little experience with it.