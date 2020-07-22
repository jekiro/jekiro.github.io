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

Beginning research on the binary