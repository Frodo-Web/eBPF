# Program and eBPF (user space)

## uprobes and shared libraries
This attaches to every malloc() call executed by any application that uses libc.so.6. 
```
SEC("uprobe/libc.so.6:malloc")
```
This only works for dynamically linked binaries that use libc.so.6. If the program is statically linked to its own libc, it won't work until you specify the program itself.

This works because the Linux kernel’s uprobe mechanism can resolve sonames (shared object names), like libc.so.6, based on where they’re mapped in memory, so you don't need to specify full path.


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
This tells perf to attach a user-space probe (uprobe) at the symbol malloc inside /usr/bin/python3.
```
sudo perf probe -x /usr/bin/python3 malloc
```
- Python may have its own internal symbol named malloc, perhaps for wrapping or debugging.
- Or it could be a PLT (Procedure Linkage Table) stub , which is how calls to malloc are resolved dynamically when calling into libc.
- But this is NOT the actual malloc implementation — that lives in libc.so.6.
### Go
```
file /lib/go-1.22/bin/go
..
/lib/go-1.22/bin/go: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=NaY_ztiU3LVZa2ji7gGb/BVafZ6p0TFQDhlr26dey/GDhy7NgRyoIxk9Nb4BU_/OzCYuwTwGmoJDQmAoNlQ, stripped
```
### What languages also use libc?
- Ruby (All memory allocations, threads, and syscalls go through libc)
- PHP
- Perl
- Python/
- Node.js / Javascript (V8)
- Rust (But you can build no_std binaries that avoid libc, The musl target allows statically linking with musl, a lightweight libc alternative)
- C/C++ (untill syscalls explicitly specified)
### What languages don't use libc?
- Golang (You usually get a static binary, Go runtime makes direct syscalls instead of going through libc, Go also has its own memory allocator and scheduler. But seems like its possible to build goland with shared libc or musl)
