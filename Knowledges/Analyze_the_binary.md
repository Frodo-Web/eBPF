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
#### readelf
readelf - display information about ELF files

-a prints absolutely everything. Unfortunately, go is builded statically (you can't see the required shared libraries) and builded without symbols and debug info. So, no symbs, no dynamic sections, no relocations.
```
readelf -a  /lib/go-1.22/bin/go
..
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x4778a0
  Start of program headers:          64 (bytes into file)
  Start of section headers:          11700272 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         6
  Size of section headers:           64 (bytes)
  Number of section headers:         14
  Section header string table index: 13

Section Headers:
  [Nr] Name              Type             Address           Offset
       Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL             0000000000000000  00000000
       0000000000000000  0000000000000000           0     0     0
  [ 1] .text             PROGBITS         0000000000401000  00001000
       0000000000590f19  0000000000000000  AX       0     0     32
  [ 2] .rodata           PROGBITS         0000000000992000  00592000
       00000000002295f4  0000000000000000   A       0     0     32
  [ 3] .typelink         PROGBITS         0000000000bbb600  007bb600
       00000000000038b8  0000000000000000   A       0     0     32
  [ 4] .itablink         PROGBITS         0000000000bbeec0  007beec0
       0000000000001540  0000000000000000   A       0     0     32
  [ 5] .gosymtab         PROGBITS         0000000000bc0400  007c0400
       0000000000000000  0000000000000000   A       0     0     1
  [ 6] .gopclntab        PROGBITS         0000000000bc0400  007c0400
       0000000000319398  0000000000000000   A       0     0     32
  [ 7] .go.buildinfo     PROGBITS         0000000000eda000  00ada000
       0000000000000170  0000000000000000  WA       0     0     16
  [ 8] .noptrdata        PROGBITS         0000000000eda180  00ada180
       0000000000033b02  0000000000000000  WA       0     0     32
  [ 9] .data             PROGBITS         0000000000f0dca0  00b0dca0
       000000000001ab08  0000000000000000  WA       0     0     32
  [10] .bss              NOBITS           0000000000f287c0  00b287a8
       00000000000648f0  0000000000000000  WA       0     0     32
  [11] .noptrbss         NOBITS           0000000000f8d0c0  00b287a8
       0000000000006920  0000000000000000  WA       0     0     32
  [12] .note.go.buildid  NOTE             0000000000400f9c  00000f9c
       0000000000000064  0000000000000000   A       0     0     4
  [13] .shstrtab         STRTAB           0000000000000000  00b287a8
       0000000000000081  0000000000000000           0     0     1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  D (mbind), l (large), p (processor specific)

There are no section groups in this file.

Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000400040 0x0000000000400040
                 0x0000000000000150 0x0000000000000150  R      0x1000
  NOTE           0x0000000000000f9c 0x0000000000400f9c 0x0000000000400f9c
                 0x0000000000000064 0x0000000000000064  R      0x4
  LOAD           0x0000000000000000 0x0000000000400000 0x0000000000400000
                 0x0000000000591f19 0x0000000000591f19  R E    0x1000
  LOAD           0x0000000000592000 0x0000000000992000 0x0000000000992000
                 0x0000000000547798 0x0000000000547798  R      0x1000
  LOAD           0x0000000000ada000 0x0000000000eda000 0x0000000000eda000
                 0x000000000004e7a8 0x00000000000b99e0  RW     0x1000
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x8

 Section to Segment mapping:
  Segment Sections...
   00
   01     .note.go.buildid
   02     .text .note.go.buildid
   03     .rodata .typelink .itablink .gosymtab .gopclntab
   04     .go.buildinfo .noptrdata .data .bss .noptrbss
   05

There is no dynamic section in this file.

There are no relocations in this file.
No processor specific unwind information to decode

No version information found in this file.

Displaying notes found in: .note.go.buildid
  Owner                Data size        Description
  Go                   0x00000053       GO BUILDID
   description data: 4e 61 59 5f 7a 74 69 55 33 4c 56 5a 61 32 6a 69 37 67 47 62 2f 42 56 61 66 5a 36 70 30 54 46 51 44 68 6c 72 32 36 64 65 79 2f 47 44 68 79 37 4e 67 52 79 6f 49 78 6b 39 4e 62 34 42 55 5f 2f 4f 7a 43 59 75 77 54 77 47 6d 6f 4a 44 51 6d 41 6f 4e 6c 51
```
#### objdump
objdump - display information from object files

For example, dynamic relocations:
```
objdump -R /usr/bin/python3 | less
```
readelf is more comfortable with -a option. But objdump can disassemble binaries!
#### nm
nm - list symbols from object files

For example, dynamic symbs
```
nm -D /usr/bin/python3 | less
```
### 🛠️ Comparison: `readelf` vs `objdump` vs `nm`

| Feature / Tool       | `readelf`                          | `objdump`                            | `nm`                                  |
|----------------------|------------------------------------|---------------------------------------|----------------------------------------|
| **Primary Purpose**  | Display ELF file structure         | Disassemble object files              | List symbols in object files           |
| **Best For**         | Viewing headers, sections, symbols | Viewing assembly code                 | Quick symbol listing                   |
| **Disassembly**      | ❌ No                              | ✅ Yes (`-d`, `-M intel`)             | ❌ No                                  |
| **Display ELF Headers** | ✅ Yes (`-h`, `-l`)             | ⚠️ Limited                           | ❌ No                                  |
| **Section Headers**  | ✅ Yes (`-S`)                     | ✅ Yes (`-x`, `-t`)                   | ❌ No                                  |
| **Program Headers**  | ✅ Yes (`-l`)                     | ⚠️ Limited                           | ❌ No                                  |
| **Symbol Table**     | ✅ Yes (`-s`, `-W`)               | ✅ Yes (`-t`)                         | ✅ Yes                                 |
| **Relocation Info**  | ✅ Yes (`-r`)                     | ✅ Yes (`-r`)                         | ❌ No                                  |
| **Dynamic Section**  | ✅ Yes (`-d`)                     | ✅ Yes                                | ❌ No                                  |
| **String Dumping**   | ⚠️ Limited                        | ✅ Yes (`-s`, `-p`)                   | ❌ No                                  |
| **Demangling C++ Symbols** | ❌ No                        | ✅ Yes (`-C`)                        | ✅ Yes (`-C`)                          |
| **Supports Multiple File Types** | ❌ Only ELF          | ✅ Most binary formats                | ✅ Most binary formats                 |
| **Stripped Binaries?** | ⚠️ Can still show some info    | ⚠️ Can disassemble, but hard to read | ❌ Symbols missing if stripped         |
| **Useful Flags**     | `-a` (all), `-S` (sections), `-s` (symbols), `-h` (header), `-d` (dynamic) | `-d` (disasm), `-M intel` (Intel syntax), `-s` (strings), `-x` (all headers) | `-C` (demangle), `-g` (debug), `-u` (undefined only) |
| **Example Use Case** | Analyzing binary dependencies or layout | Reverse-engineering or viewing assembly | Finding function names and addresses   |
