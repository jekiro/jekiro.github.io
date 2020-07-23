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
Files: [chezzz](/assets/files/chezzz)
>I'll also give you the flag if you beat me in chess  
>nc 2020.redpwnc.tf 31611

## Basic Research and Static Analysis

Beginning research on the binary, by checking the filetype it's pretty obvious that it's a 64 bit ELF executable.  

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
we can ignore sub_12B8 somewhat, and also calls a bigger function that is at sub_159A. As you may also notice rax gets moved into rdi for every function called and in the main function it points to an allocated structure on the stack of size 0x408 or so. That will be useful knowledge to come to understand how the binary works. 

![](/content/OEP/chezzz/sub_1b8a.PNG)

Looking at **sub_159A** it is pretty obvious that it is doing most of the handling for the chess board just from the size. 

![](/content/OEP/chezzz/sub_159a_graph.PNG)

While a function that is large, and has calls to other functions might seem daunting, looking through it slowly, one of the very first and obvious things that caught my eye was the call to **system**.

![](/content/OEP/chezzz/sub_159a_system.PNG)

Tracing the system call backwards shows it depends on the returning value from **sub_2792** equaling **467 (0x1D3)**. I renamed sub_2792 to **f_checkwin** to make it more understandable.

![](/content/OEP/chezzz/sub_159a_2792.PNG)

The win check function has a jump table that leads to different code blocks depending on the return of the function **sub_1272**.  
This isn't being detected by IDA so you can create a manual definition for a switch idiom by clicking where it starts which is the ja instruction for this example and setting the values correctly.

![](/content/OEP/chezzz/win_ex.PNG)

![](/content/OEP/chezzz/win_switch.PNG)

The 6 different cases are not obvious as to what they do so at this point I decided to get information from dynamically analysing the binary rather than going through and guessing what the structures may be.

## Filling missing information with Dynamic Analysis

From the information gathered in the previous section, and the knowledge of a large section of memory on the stack that is most likely the chess board structure, run the program in gdb and breakpoint somewhere when rax gets set as a pointer to the board. Without ASLR on, a command for that in GDB is  
**break *(0x555555554000+0x1BA6)**  

After breaking and locating the address, since we know the size of the structure you can easily print out the hex with the GDB command x/128xg where 128 is the number of 8 byte hex values to print from the address passed. 

>x/256xw 0x7fffffffdde0

```
0x7fffffffdde0:	0x00000004	0x00000000	0x00000000	0x00000000
0x7fffffffddf0:	0x00000003	0x00000000	0x00000000	0x00000001
0x7fffffffde00:	0x00000002	0x00000000	0x00000000	0x00000002
0x7fffffffde10:	0x00000001	0x00000000	0x00000000	0x00000003
0x7fffffffde20:	0x00000000	0x00000000	0x00000000	0x00000004
0x7fffffffde30:	0x00000002	0x00000000	0x00000000	0x00000005
0x7fffffffde40:	0x00000003	0x00000000	0x00000000	0x00000006
0x7fffffffde50:	0x00000004	0x00000000	0x00000000	0x00000007
0x7fffffffde60:	0x00000005	0x00000000	0x00000001	0x00000000
0x7fffffffde70:	0x00000005	0x00000000	0x00000001	0x00000001
0x7fffffffde80:	0x00000005	0x00000000	0x00000001	0x00000002
0x7fffffffde90:	0x00000005	0x00000000	0x00000001	0x00000003
0x7fffffffdea0:	0x00000005	0x00000000	0x00000001	0x00000004
0x7fffffffdeb0:	0x00000005	0x00000000	0x00000001	0x00000005
0x7fffffffdec0:	0x00000005	0x00000000	0x00000001	0x00000006
0x7fffffffded0:	0x00000005	0x00000000	0x00000001	0x00000007
0x7fffffffdee0:	0x00000006	0x00000002	0x00000002	0x00000000
...
0x7fffffffe0d0:	0x00000006	0x00000002	0x00000005	0x00000007
0x7fffffffe0e0:	0x00000005	0x00000001	0x00000006	0x00000000
0x7fffffffe0f0:	0x00000005	0x00000001	0x00000006	0x00000001
0x7fffffffe100:	0x00000005	0x00000001	0x00000006	0x00000002
0x7fffffffe110:	0x00000005	0x00000001	0x00000006	0x00000003
0x7fffffffe120:	0x00000005	0x00000001	0x00000006	0x00000004
0x7fffffffe130:	0x00000005	0x00000001	0x00000006	0x00000005
0x7fffffffe140:	0x00000005	0x00000001	0x00000006	0x00000006
0x7fffffffe150:	0x00000005	0x00000001	0x00000006	0x00000007
0x7fffffffe160:	0x00000004	0x00000001	0x00000007	0x00000000
0x7fffffffe170:	0x00000003	0x00000001	0x00000007	0x00000001
0x7fffffffe180:	0x00000002	0x00000001	0x00000007	0x00000002
0x7fffffffe190:	0x00000001	0x00000001	0x00000007	0x00000003
0x7fffffffe1a0:	0x00000000	0x00000001	0x00000007	0x00000004
0x7fffffffe1b0:	0x00000002	0x00000001	0x00000007	0x00000005
0x7fffffffe1c0:	0x00000003	0x00000001	0x00000007	0x00000006
0x7fffffffe1d0:	0x00000004	0x00000001	0x00000007	0x00000007
```

The patterns are pretty obvious to see, but for example this is the layout I noticed.

```
0x7fffffffe130:	0x00000005(piece_type)	0x00000001(side)	0x00000006(position_y)	0x00000005(position_x)
```

With a structure laid out and known we can create a struct in the local types view for IDA, and my structures are as seen below.

```cpp
struct struct_piece
{
  _DWORD piece_type;
  _DWORD piece_side;
  _DWORD y_axis;
  _DWORD x_axis;
};

struct struct_board
{
  struct_piece spots[64];
  _DWORD whosturn;
};
```

board->whosturn is used to figure out which side's turn it is, and is toggled between 1 and 0 during the execution of the program whenever a turn is finished.  

Now that a structure is laid out in IDA, any time the board is used it will show a more relevant and understandable piece of information in the decompiler as long as you set the var type.  
The checkwin function makes more sense here, both the get_piece_type and get_piece_side functions are simple functions that just retrieve the type or side from the piece. And the piece type is used to determine what calculation to do based on the position on the board for that specific piece type. I took the liberty of commenting what the functions do as they are simple and it would be tedious, feel free to download and look into it if you need to.
```cpp
__int64 __fastcall f_checkwin(struct_board *board)
{
  unsigned int type; // ST28_4
  unsigned int needtobe467; // [rsp+1Ch] [rbp-14h]
  signed int i; // [rsp+20h] [rbp-10h]
  signed int j; // [rsp+24h] [rbp-Ch]

  needtobe467 = 0;
  for ( i = 0; i <= 7; ++i )
  {
    for ( j = 0; j <= 7; ++j )
    {
      type = get_piece_type(&board->spots[8LL * i + j]);
      get_piece_side(&board->spots[8LL * i + j]);
      switch ( (unsigned __int64)type )
      {
        case 0uLL:
          needtobe467 += add_2_3((__int64)board, 8 - i, j + 9);// var_2 + var_3
          break;
        case 1uLL:
          needtobe467 += mul_2_3((__int64)board, 8 - i, j + 9);// var_2 * var_3
          break;
        case 2uLL:
          needtobe467 += mul_double_2_3((__int64)board, 8 - i, j + 9);// 2*(var_2+var_3)
          break;
        case 3uLL:
          needtobe467 += mod_3_2((__int64)board, 8 - i, j + 9);// var_3 % var_2
          break;
        case 4uLL:
          needtobe467 += sub_2760((__int64)board, 8 - i, j + 9);// 256 - var_2 - var_3
          break;
        case 5uLL:
          needtobe467 += subt_2_3((__int64)board, 8 - i, j + 9);// var_2 - var_3
          break;
        default:
          continue;
      }
    }
  }
  return needtobe467;
}
```

## Creating a Z3 script to calculate a correct path

Knowing the path to win, and the mathematical requirements, I did not want to go through it manually so I enlisted the help of my teammate kosinw for the Z3 side of the challenge. The final script for reference is avaliable [here](/assets/files/chezzz.py). 

It sets up the board with an 8x8 array of integers, limiting the values for each piece to 0 to 6 and restricting the number of existing pieces depending on the settings. It also limits the game by the rules that exist, which for some reason that is just up to the developer, is that kings are unmovable.  
Then the script implements restrictions for the type of piece and what calculation needs to be done for that specific piece, and restricts it to equal 467.  
An example from the final script is shown, with all the pieces in place for the required patterns to generate 467:  

```
_ _ Q _ K _ _ _
_ _ _ _ _ _ Q _
_ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _
_ _ _ _ K _ _ R
```

And it works, yielding the flag directly to us.

![](/content/OEP/chezzz/flag.PNG)

### Credits

Credits to my teammate **_kosinw_** for helping with Z3 since I have little experience with it.