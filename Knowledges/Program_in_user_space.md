# Program and eBPF (user space)

## uprobes and shared libraries
This attaches to every malloc() call executed by any application that uses libc.so.6. 
```
SEC("uprobe/libc.so.6:malloc")
```
This only works for dynamically linked binaries that use libc.so.6. If the program is statically linked to its own libc, it won't work until you specify the program itself.
## Program Languages and shared libraries
### Python
```
ldd /usr/bin/python3
..
        linux-vdso.so.1 (0x00007ffd1a0ed000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f6dcde7a000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f6dcde5e000)
        libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007f6dcde32000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f6dcdc20000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f6dcdf6a000)
```
#### malloc example
Python uses different malloc call, which is like a wrap over libc maloc, you can see this
```
nm -D /lib/x86_64-linux-gnu/libc.so.6 | grep malloc
..
00000000000ad650 T __libc_malloc@@GLIBC_2.2.5
000000000020a140 V __malloc_hook@GLIBC_2.2.5
000000000020a160 B __malloc_initialize_hook@GLIBC_2.2.5
00000000000ad650 T malloc@@GLIBC_2.2.5
00000000000af4c0 W malloc_info@@GLIBC_2.10
00000000000af050 W malloc_stats@@GLIBC_2.2.5
00000000000aeba0 W malloc_trim@@GLIBC_2.2.5
00000000000aee70 W malloc_usable_size@@GLIBC_2.2.5

nm -D /usr/bin/python3 | grep malloc
..
00000000004f960d T PyInit__tracemalloc
                 U malloc@GLIBC_2.2.5
```
### Go
```
file /lib/go-1.22/bin/go
..
/lib/go-1.22/bin/go: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=NaY_ztiU3LVZa2ji7gGb/BVafZ6p0TFQDhlr26dey/GDhy7NgRyoIxk9Nb4BU_/OzCYuwTwGmoJDQmAoNlQ, stripped
```
