# Analyze the binary
## Tools
#### strings
strings - print the strings of printable characters in files.
```
strings  /lib/go-1.22/bin/go | less
..
NaY_ztiU3LVZa2ji7gGb/BVafZ6p0TFQDhlr26dey/GDhy7NgRyoIxk9Nb4BU_/OzCYuwTwGmoJDQmAoNlQ
D$ H
|$(H
vSUH
v`UH
...
runtime/malloc.go
...
.noptrdata
.data
.bss
.noptrbss
.note.go.buildid
```
